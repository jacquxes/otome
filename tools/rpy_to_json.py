#!/usr/bin/env python3
"""
rpy_to_json.py - turn Ren'Py script files into data the Godot story player can read.

You keep writing the story in Ren'Py. Re-run this after you change a script.

Usage (from the repo root):

    python3 tools/rpy_to_json.py game godot                       (the whole game)
    python3 tools/rpy_to_json.py game godot --only musician_1     (one label, for testing)
    python3 tools/rpy_to_json.py game godot --scripts script_04_musician.rpy

What it writes into the Godot project folder:

    story/<script name>.json   the story, as a flat list of steps
    story/game_data.json       characters, image names, starting values
    story/report.txt           every line it could NOT convert (nothing is dropped silently)
    assets/game/...            copies of the images, fonts and UI art the story uses

What it converts:  dialogue, show / scene / hide (with simple ATL), pause, menus,
if / elif / else, while, `$` one-line Python, jump, call, return, play, stop,
`call screen` (opens the Godot scene with that name).

What it does not convert (listed in report.txt for porting by hand):
screen layouts, `python:` blocks, functions, layered images, custom transforms.
"""

import argparse
import ast
import json
import os
import re
import shutil
import sys

# ----------------------------------------------------------------------------
# 1. Read a .rpy file into a tree of lines, using the indentation
# ----------------------------------------------------------------------------


class Line:
    def __init__(self, indent, text, number):
        self.indent = indent
        self.text = text
        self.number = number
        self.children = []


def strip_comment(text):
    """Remove a trailing # comment, but not a # inside a string."""
    quote = None
    i = 0
    while i < len(text):
        c = text[i]
        if quote:
            if c == "\\":
                i += 1
            elif c == quote:
                quote = None
        elif c in "\"'":
            quote = c
        elif c == "#":
            return text[:i]
        i += 1
    return text


def bracket_balance(text):
    """How many brackets are still open at the end of this text."""
    depth = 0
    quote = None
    i = 0
    while i < len(text):
        c = text[i]
        if quote:
            if c == "\\":
                i += 1
            elif c == quote:
                quote = None
        elif c in "\"'":
            quote = c
        elif c in "([{":
            depth += 1
        elif c in ")]}":
            depth -= 1
        i += 1
    return depth


def read_tree(path):
    with open(path, encoding="utf-8-sig") as f:
        raw = f.read().split("\n")

    # Join lines that continue inside brackets (multi-line dicts and lists).
    logical = []
    i = 0
    while i < len(raw):
        text = strip_comment(raw[i]).rstrip()
        number = i + 1
        while bracket_balance(text) > 0 and i + 1 < len(raw):
            i += 1
            text += " " + strip_comment(raw[i]).strip()
        i += 1
        if text.strip():
            indent = len(text) - len(text.lstrip(" "))
            logical.append(Line(indent, text.strip(), number))

    root = Line(-1, "", 0)
    stack = [root]
    for line in logical:
        while stack[-1].indent >= line.indent:
            stack.pop()
        stack[-1].children.append(line)
        stack.append(line)
    return root


def source_of(line, depth=0):
    """The original text of a line and everything under it (for the report)."""
    out = ["    " * depth + line.text]
    for child in line.children:
        out.extend(source_of(child, depth + 1))
    return out


# ----------------------------------------------------------------------------
# 2. Python expressions -> Godot expressions
# ----------------------------------------------------------------------------


class CannotConvert(Exception):
    pass


BIN_OPS = {ast.Add: "+", ast.Sub: "-", ast.Mult: "*", ast.Div: "/", ast.Mod: "%"}
CMP_OPS = {
    ast.Eq: "==", ast.NotEq: "!=", ast.Lt: "<", ast.LtE: "<=", ast.Gt: ">",
    ast.GtE: ">=", ast.In: "in", ast.Is: "==", ast.IsNot: "!=",
}
# Python method name -> Godot method name
METHOD_NAMES = {"remove": "erase", "items": "keys"}


def to_godot(node):
    """Write a Python expression (already parsed) as a Godot expression."""
    if isinstance(node, ast.Constant):
        v = node.value
        if v is True:
            return "true"
        if v is False:
            return "false"
        if v is None:
            return "null"
        if isinstance(v, str):
            return json.dumps(v, ensure_ascii=False)
        if isinstance(v, (int, float)):
            return repr(v)
        raise CannotConvert("constant " + repr(v))
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.BinOp) and type(node.op) in BIN_OPS:
        return "(%s %s %s)" % (to_godot(node.left), BIN_OPS[type(node.op)], to_godot(node.right))
    if isinstance(node, ast.BoolOp):
        word = " and " if isinstance(node.op, ast.And) else " or "
        return "(" + word.join(to_godot(v) for v in node.values) + ")"
    if isinstance(node, ast.UnaryOp):
        if isinstance(node.op, ast.Not):
            return "(not %s)" % to_godot(node.operand)
        if isinstance(node.op, ast.USub):
            return "(-%s)" % to_godot(node.operand)
    if isinstance(node, ast.Compare):
        parts = []
        left = node.left
        for op, right in zip(node.ops, node.comparators):
            if isinstance(op, ast.NotIn):
                parts.append("(not (%s in %s))" % (to_godot(left), to_godot(right)))
            elif type(op) in CMP_OPS:
                parts.append("(%s %s %s)" % (to_godot(left), CMP_OPS[type(op)], to_godot(right)))
            else:
                raise CannotConvert("comparison")
            left = right
        return parts[0] if len(parts) == 1 else "(" + " and ".join(parts) + ")"
    if isinstance(node, ast.Subscript):
        return "%s[%s]" % (to_godot(node.value), to_godot(node.slice))
    if isinstance(node, ast.Attribute):
        return "%s.%s" % (to_godot(node.value), node.attr)
    if isinstance(node, ast.Dict):
        pairs = ["%s: %s" % (to_godot(k), to_godot(v)) for k, v in zip(node.keys, node.values)]
        return "{" + ", ".join(pairs) + "}"
    if isinstance(node, (ast.List, ast.Tuple)):
        return "[" + ", ".join(to_godot(e) for e in node.elts) + "]"
    if isinstance(node, ast.Call):
        if node.keywords:
            raise CannotConvert("keyword arguments")
        args = [to_godot(a) for a in node.args]
        f = node.func
        if isinstance(f, ast.Name):
            if f.id == "len" and len(args) == 1:
                return "%s.size()" % args[0]
            return "%s(%s)" % (f.id, ", ".join(args))
        if isinstance(f, ast.Attribute):
            owner_src = ast.unparse(f.value)
            if owner_src == "renpy.random" and f.attr == "randint":
                return "randi_range(%s)" % ", ".join(args)
            if owner_src == "renpy.random" and f.attr == "choice":
                return "%s.pick_random()" % args[0]
            if owner_src.startswith("renpy"):
                raise CannotConvert("renpy." + f.attr)
            owner = to_godot(f.value)
            if f.attr == "update" and len(args) == 1:
                return "%s.merge(%s, true)" % (owner, args[0])
            return "%s.%s(%s)" % (owner, METHOD_NAMES.get(f.attr, f.attr), ", ".join(args))
    raise CannotConvert(type(node).__name__)


def expr_to_godot(source):
    try:
        tree = ast.parse(source.strip(), mode="eval")
    except SyntaxError:
        raise CannotConvert("not a Python expression")
    return to_godot(tree.body)


def target_path(node):
    """`encounters["musician"]` -> root "encounters", keys ['"musician"']."""
    keys = []
    while True:
        if isinstance(node, ast.Subscript):
            keys.insert(0, to_godot(node.slice))
            node = node.value
        elif isinstance(node, ast.Attribute):
            # persistent.flag = True  is stored as  persistent["flag"]
            keys.insert(0, json.dumps(node.attr))
            node = node.value
        elif isinstance(node, ast.Name):
            return node.id, keys
        else:
            raise CannotConvert("assignment target")


def python_line_to_op(source):
    """One `$ ...` line -> one step."""
    try:
        tree = ast.parse(source.strip())
    except SyntaxError:
        raise CannotConvert("not valid Python")
    if len(tree.body) != 1:
        raise CannotConvert("more than one statement")
    stmt = tree.body[0]
    if isinstance(stmt, ast.Assign) and len(stmt.targets) == 1:
        root, keys = target_path(stmt.targets[0])
        return {"t": "set", "var": root, "keys": keys, "op": "=", "value": to_godot(stmt.value)}
    if isinstance(stmt, ast.AugAssign) and type(stmt.op) in BIN_OPS:
        root, keys = target_path(stmt.target)
        return {"t": "set", "var": root, "keys": keys,
                "op": BIN_OPS[type(stmt.op)] + "=", "value": to_godot(stmt.value)}
    if isinstance(stmt, ast.Expr) and isinstance(stmt.value, ast.Call):
        return {"t": "eval", "code": to_godot(stmt.value)}
    raise CannotConvert(type(stmt).__name__)


# ----------------------------------------------------------------------------
# 3. Story statements -> a flat list of steps
# ----------------------------------------------------------------------------

STRING = r'"((?:[^"\\]|\\.)*)"'
SAY_RE = re.compile(r'^(?:(\w+)((?:\s+\w+)*)\s+)?' + STRING + r'(?:\s+with\s+(.+))?$')
WARPERS = {"linear", "ease", "easein", "easeout"}
# Effects that need a shader in Godot. The picture still shows; the effect is left out for now.
ATL_LATER = {"blur", "matrixcolor"}
ATL_PROPS = {"xalign", "yalign", "xpos", "ypos", "zoom", "xzoom", "yzoom", "alpha", "xanchor", "yanchor",
             "xoffset", "yoffset", "rotate", "zpos"}


def unescape(text):
    return text.replace('\\"', '"').replace("\\n", "\n").replace("\\'", "'")


class Converter:
    def __init__(self, characters):
        self.characters = characters
        self.ops = []
        self.labels = {}
        self.label_order = []
        self.todo = []          # (file, line number, source text, reason)
        self.skipped = []       # (file, line number, effect left out)
        self.current_label = ""
        self.python_count = 0
        self.python_blocks = [] # (file, line number, function name, code)
        self.screens = set()    # screens the story opens with `call screen`
        self.file = ""

    # -- helpers --------------------------------------------------------------

    def emit(self, op, line=None):
        if line is not None:
            op["line"] = line.number
        self.ops.append(op)
        return len(self.ops) - 1

    def unsupported(self, line, reason):
        text = "\n".join(source_of(line))
        self.todo.append((self.file, line.number, text, reason))
        self.emit({"t": "todo", "code": text, "why": reason}, line)

    def condition(self, source, line):
        try:
            return expr_to_godot(source)
        except CannotConvert as e:
            self.todo.append((self.file, line.number, line.text, "condition: %s" % e))
            return None

    # -- blocks ---------------------------------------------------------------

    def block(self, lines):
        i = 0
        while i < len(lines):
            line = lines[i]
            text = line.text
            if re.match(r"^if\b", text):
                chain = [line]
                while i + 1 < len(lines) and re.match(r"^(elif\b|else\s*:)", lines[i + 1].text):
                    i += 1
                    chain.append(lines[i])
                self.if_chain(chain)
            else:
                self.statement(line)
            i += 1

    def if_chain(self, chain):
        end_jumps = []
        for line in chain:
            head = line.text.rstrip(":").strip()
            cond_src = re.sub(r"^(if|elif|else)\b", "", head).strip()
            skip = None
            if cond_src:
                cond = self.condition(cond_src, line)
                if cond is None:
                    self.unsupported(line, "condition could not be converted")
                    continue
                skip = self.emit({"t": "jump_if_not", "cond": cond, "to": -1}, line)
            self.block(line.children)
            end_jumps.append(self.emit({"t": "goto", "to": -1}))
            if skip is not None:
                self.ops[skip]["to"] = len(self.ops)
        for j in end_jumps:
            self.ops[j]["to"] = len(self.ops)

    # -- single statements ----------------------------------------------------

    def statement(self, line):
        text = line.text
        word = text.split()[0].rstrip(":") if text.split() else ""

        m = re.match(r"^label\s+([\w.]+)\s*(\(.*\))?\s*:$", text)
        if m:
            name = m.group(1)
            self.labels[name] = len(self.ops)
            self.label_order.append(name)
            self.current_label = name
            self.python_count = 0
            self.block(line.children)
            return

        if text.startswith("$"):
            try:
                self.emit(python_line_to_op(text[1:]), line)
            except CannotConvert as e:
                self.unsupported(line, "Python: %s" % e)
            return

        if text in ("python:", "python hide:"):
            # Python blocks are ported by hand as a function in state.gd.
            # Its name is py_<label>_<number>, e.g. py_reset_daily_visits_1.
            self.python_count += 1
            name = "py_%s_%d" % (self.current_label.replace(".", "_"), self.python_count)
            code = "\n".join("\n".join(source_of(c)) for c in line.children)
            self.python_blocks.append((self.file, line.number, name, code))
            self.emit({"t": "python", "func": name, "code": code}, line)
            return

        if word in ("define", "default", "image", "transform", "camera"):
            return  # setup lines: read once for game_data.json, nothing to do while playing

        if word == "while":
            cond = self.condition(text[5:].rstrip(":"), line)
            if cond is None:
                return self.unsupported(line, "condition could not be converted")
            top = self.emit({"t": "jump_if_not", "cond": cond, "to": -1}, line)
            self.block(line.children)
            self.emit({"t": "goto", "to": top})
            self.ops[top]["to"] = len(self.ops)
            return

        if word == "menu":
            return self.menu(line)

        if word in ("show", "scene", "hide"):
            return self.show(line, word)

        if word == "with":
            self.emit({"t": "with", "name": text[4:].strip()}, line)
            return

        if word == "pause":
            rest = text[5:].strip()
            try:
                self.emit({"t": "pause", "time": float(rest) if rest else None}, line)
            except ValueError:
                self.unsupported(line, "pause time is not a plain number")
            return

        if word == "window":
            self.emit({"t": "window", "show": "hide" not in text.split()}, line)
            return

        if word == "return":
            self.emit({"t": "return"}, line)
            return

        if word in ("jump", "call"):
            return self.jump_or_call(line, word)

        if word in ("play", "queue"):
            return self.play(line)

        if word == "stop":
            m = re.match(r"^stop\s+(\w+)(?:\s+fadeout\s+([\d.]+))?$", text)
            if m:
                self.emit({"t": "stop", "channel": m.group(1),
                           "fadeout": float(m.group(2) or 0)}, line)
            else:
                self.unsupported(line, "stop statement form")
            return

        if word == "pass":
            return

        m = SAY_RE.match(text)
        if m and not line.children:
            who, attrs, what, _with = m.groups()
            if who is None or who in self.characters or who == "extend":
                self.emit({"t": "say", "who": who, "attrs": (attrs or "").split(),
                           "text": unescape(what)}, line)
                return
            return self.unsupported(line, "speaker '%s' is not a defined Character" % who)

        self.unsupported(line, "statement not supported yet")

    def jump_or_call(self, line, word):
        text = re.sub(r"\s+from\s+\w+$", "", line.text)
        rest = text[len(word):].strip()
        if rest.startswith("screen"):
            m = re.match(r"^screen\s+(\w+)\s*(\(.*?\))?(\s+with\s+\S+)?$", rest)
            if not m or word != "call":
                return self.unsupported(line, "screen call form")
            self.screens.add(m.group(1))
            self.emit({"t": "screen", "name": m.group(1)}, line)
            return
        if rest.startswith("expression"):
            try:
                code = expr_to_godot(rest[len("expression"):])
            except CannotConvert as e:
                return self.unsupported(line, "expression: %s" % e)
            self.emit({"t": word + "_expr", "code": code}, line)
        elif re.match(r"^[\w.]+$", rest):
            self.emit({"t": word, "label": rest}, line)
        else:
            self.unsupported(line, "%s with arguments" % word)

    def play(self, line):
        m = re.match(r'^(play|queue)\s+(\w+)\s+"([^"]+)"(.*)$', line.text)
        if not m:
            return self.unsupported(line, "play statement form")
        _, channel, name, rest = m.groups()
        op = {"t": "play", "channel": channel, "file": name, "from": 0.0}
        tag = re.match(r"^<from\s+([\d.]+)(?:\s+to\s+([\d.]+))?>(.*)$", name)
        if tag:
            op["from"] = float(tag.group(1))
            if tag.group(2):
                op["to"] = float(tag.group(2))
            op["file"] = tag.group(3)
        fade = re.search(r"fadein\s+([\d.]+)", rest)
        op["fadein"] = float(fade.group(1)) if fade else 0.0
        op["if_changed"] = "if_changed" in rest
        op["loop"] = "noloop" not in rest and (channel == "music" or " loop" in rest)
        self.emit(op, line)

    def show(self, line, word):
        text = line.text.rstrip(":").strip()
        rest = text[len(word):].strip()
        if rest.startswith("screen") or rest.startswith("expression") or rest.startswith("layer"):
            return self.unsupported(line, "%s %s - port by hand" % (word, rest.split()[0]))
        op = {"t": word}
        m = re.match(r"^text\s+" + STRING, rest)
        if m:
            op["text"] = unescape(m.group(1))
            rest = "text" + rest[m.end():]
        m = re.search(r"\s+with\s+(\S.*)$", rest)
        if m:
            op["with"] = m.group(1).strip()
            rest = rest[:m.start()]
        m = re.search(r"\s+at\s+(.+)$", rest)
        if m:
            op["at"] = [a.strip() for a in m.group(1).split(",")]
            rest = rest[:m.start()]
        m = re.search(r"\s+zorder\s+(-?[\d.]+)", rest)
        if m:
            op["zorder"] = int(float(m.group(1)))
            rest = rest[:m.start()] + rest[m.end():]
        for clause in ("behind", "as", "onlayer"):
            if re.search(r"\s+%s\s+" % clause, " " + rest + " "):
                return self.unsupported(line, "'%s' clause" % clause)
        op["image"] = rest.strip()
        if word == "scene" and not op["image"]:
            op["image"] = None
        if line.children:
            atl, problem = self.atl(line.children, line)
            if problem:
                return self.unsupported(line, "ATL: " + problem)
            op["atl"] = atl
        self.emit(op, line)

    def atl(self, lines, owner):
        """Simple ATL only: property lines, and warper lines like `linear 2.0 xalign 1.0`."""
        steps = []
        for line in lines:
            if line.children:
                return None, "nested block (%s)" % line.text
            tokens = line.text.split()
            step = {"warp": None, "time": 0.0, "props": {}}
            if tokens[0] == "pause" and len(tokens) == 2:
                try:
                    steps.append({"wait": float(tokens[1])})
                    continue
                except ValueError:
                    return None, line.text
            if tokens[0] in WARPERS:
                try:
                    step["warp"] = tokens[0]
                    step["time"] = float(tokens[1])
                except (IndexError, ValueError):
                    return None, line.text
                tokens = tokens[2:]
            if len(tokens) % 2:
                return None, line.text
            for name, value in zip(tokens[0::2], tokens[1::2]):
                if name in ATL_LATER:
                    self.skipped.append((self.file, owner.number, "%s %s" % (name, value)))
                    continue
                if name not in ATL_PROPS:
                    return None, "property '%s'" % name
                try:
                    number = float(value)
                except ValueError:
                    return None, "value '%s'" % value
                # Ren'Py rule: `xpos 100` is pixels, `xpos 0.5` is half the screen.
                if name in ("xpos", "ypos") and "." not in value:
                    name += "_px"
                step["props"][name] = number
            steps.append(step)
        return steps, None

    def menu(self, line):
        op = {"t": "menu", "prompt": None, "choices": []}
        index = self.emit(op, line)
        end_jumps = []
        for item in line.children:
            m = re.match(r"^" + STRING + r"(?:\s+if\s+(.+?))?\s*:$", item.text)
            if m:
                caption, cond_src = m.groups()
                cond = self.condition(cond_src, item) if cond_src else None
                op["choices"].append({"text": unescape(caption), "cond": cond, "to": len(self.ops)})
                self.block(item.children)
                end_jumps.append(self.emit({"t": "goto", "to": -1}))
                continue
            m = SAY_RE.match(item.text)
            if m and (m.group(1) is None or m.group(1) in self.characters):
                op["prompt"] = {"who": m.group(1), "attrs": (m.group(2) or "").split(),
                                "text": unescape(m.group(3))}
                continue
            self.todo.append((self.file, item.number, item.text, "menu line not understood"))
        for j in end_jumps:
            self.ops[j]["to"] = len(self.ops)
        if not op["choices"]:
            self.ops[index] = {"t": "todo", "code": "\n".join(source_of(line)), "why": "empty menu"}


# ----------------------------------------------------------------------------
# 4. Characters, images and starting values (read from every .rpy in game/)
# ----------------------------------------------------------------------------

IMAGE_EXT = (".png", ".jpg", ".jpeg", ".webp")


def literal_assignments(block_lines):
    """Plain `name = value` lines at the top of an `init python:` block (e.g. the gallery's `characters`)."""
    source = "\n".join("\n".join(source_of(c)) for c in block_lines)
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return {}
    found = {}
    for stmt in tree.body:
        if isinstance(stmt, ast.Assign) and len(stmt.targets) == 1 and isinstance(stmt.targets[0], ast.Name):
            try:
                ast.literal_eval(stmt.value)
                found[stmt.targets[0].id] = to_godot(stmt.value)
            except (ValueError, SyntaxError, CannotConvert):
                pass
    return found


def collect_game_data(game_dir, report):
    characters, images, tag_transforms, defaults = {}, {}, {}, {}
    persistent, gallery, game = {}, [], {}

    # Ren'Py names every file under images/ after its file name, lower case.
    images_dir = os.path.join(game_dir, "images")
    for folder, _, files in os.walk(images_dir):
        for name in sorted(files):
            if name.lower().endswith(IMAGE_EXT):
                rel = os.path.relpath(os.path.join(folder, name), game_dir).replace(os.sep, "/")
                images[os.path.splitext(name)[0].lower()] = {"path": rel}

    for name in sorted(os.listdir(game_dir)):
        if not name.endswith(".rpy"):
            continue
        tree = read_tree(os.path.join(game_dir, name))
        for line in walk(tree):
            text = line.text

            if text in ("init python:", "python early:") or re.match(r"^init\s+-?\d*\s*python:$", text):
                for key, value in literal_assignments(line.children).items():
                    defaults.setdefault(key, value)
                # The gallery: gallery.button("name"), then its image(s) and an optional condition
                for inner in line.children:
                    g = re.match(r'^gallery\.(button|image|condition)\(\s*"(.+)"\s*\)$', inner.text)
                    if not g:
                        continue
                    kind, value = g.groups()
                    if kind == "button":
                        gallery.append({"name": value, "images": [], "conditions": []})
                    elif gallery and kind == "image":
                        gallery[-1]["images"].append(value)
                    elif gallery:
                        try:
                            gallery[-1]["conditions"].append(expr_to_godot(value))
                        except CannotConvert:
                            report.append("%s:%d  gallery condition not converted: %s" % (name, inner.number, value))
                continue

            # Values that are kept between playthroughs: default persistent.x = False
            m = re.match(r"^(?:default|define)\s+persistent\.(\w+)\s*=\s*(.+)$", text)
            if m:
                try:
                    ast.literal_eval(m.group(2))
                    persistent[m.group(1)] = expr_to_godot(m.group(2))
                except (ValueError, SyntaxError, CannotConvert):
                    pass
                continue

            m = re.match(r'^define\s+config\.(name|version)\s*=\s*(?:_\()?"([^"]*)"', text)
            if m:
                game[m.group(1)] = m.group(2)
                continue

            m = re.match(r"^define\s+(\w+)\s*=\s*Character\((.*)\)$", text)
            if m:
                ident, args = m.groups()
                entry = {"name": None, "image": None, "color": None, "bubble": "kind=bubble" in args.replace(" ", "")}
                first = re.match(r'^\s*(?:_\()?"([^"]*)"', args)
                if first:
                    entry["name"] = first.group(1)
                img = re.search(r'image\s*=\s*"([^"]+)"', args)
                col = re.search(r'color\s*=\s*["\'](#[0-9a-fA-F]+)["\']', args)
                entry["image"] = img.group(1) if img else None
                entry["color"] = col.group(1) if col else None
                characters[ident] = entry
                continue

            m = re.match(r'^define\s+config\.tag_transform\["(\w+)"\]\s*=\s*Transform\((.*)\)$', text)
            if m:
                tag_transforms[m.group(1)] = {k: float(v) for k, v in re.findall(r"(\w+)\s*=\s*([\d.]+)", m.group(2))}
                continue

            m = re.match(r"^image\s+([\w ]+?)\s*=\s*(.+)$", text)
            if m:
                img_name, value = m.group(1).strip(), m.group(2).strip()
                entry = parse_image_value(value)
                if entry:
                    images[img_name] = entry
                else:
                    report.append("%s:%d  image '%s' uses a form the converter does not read: %s"
                                  % (name, line.number, img_name, value))
                continue
            if re.match(r"^image\s+[\w ]+:$", text):
                report.append("%s:%d  image '%s' is an ATL image - port by hand"
                              % (name, line.number, text[6:-1]))
                continue

            # Plain settings such as `define TIP_MIN = 4` are kept too, so the Godot
            # screens read the same numbers as Ren'Py. (Characters, transitions and
            # other non-plain defines are skipped.)
            m = re.match(r"^define\s+(\w+)\s*=\s*(.+)$", text)
            if m:
                try:
                    ast.literal_eval(m.group(2))
                    defaults.setdefault(m.group(1), expr_to_godot(m.group(2)))
                except (ValueError, SyntaxError, CannotConvert):
                    pass
                continue

            m = re.match(r"^default\s+([\w.]+)\s*=\s*(.+)$", text)
            if m and "." not in m.group(1):
                try:
                    ast.literal_eval(m.group(2))
                    # Stored as Godot source text so whole numbers stay whole numbers.
                    defaults[m.group(1)] = expr_to_godot(m.group(2))
                except (ValueError, SyntaxError, CannotConvert):
                    report.append("%s:%d  default '%s' is not a plain value - set it in state.gd"
                                  % (name, line.number, m.group(1)))

    return {"characters": characters, "images": images,
            "tag_transforms": tag_transforms, "defaults": defaults,
            "persistent": persistent, "gallery": gallery, "game": game,
            "screens": collect_screens(game_dir)}


def collect_screens(game_dir):
    """For every Ren'Py screen: the labels its buttons jump to."""
    screens = {}
    for name in sorted(os.listdir(game_dir)):
        if not name.endswith(".rpy"):
            continue
        for line in read_tree(os.path.join(game_dir, name)).children:
            m = re.match(r"^screen\s+(\w+)", line.text)
            if not m:
                continue
            body = "\n".join(source_of(line))
            jumps = []
            for target in re.findall(r'Jump\(\s*"([\w.]+)"\s*\)', body):
                if target not in jumps:
                    jumps.append(target)
            screens[m.group(1)] = {"file": name, "jumps": jumps, "returns": "Return(" in body}
    return screens


def parse_image_value(value):
    m = re.match(r'^"([^"\[]+)"$', value)
    if m:
        return {"path": m.group(1)}
    # "images/cafe/[cafe_menu[0]].png" : the file is worked out when the picture is shown
    m = re.match(r'^"([^"]+\[.+\][^"]*)"$', value)
    if m:
        return {"path": m.group(1), "dynamic": True}
    m = re.match(r'^im\.Scale\(\s*"([^"\[]+)"\s*,\s*(\d+)\s*,\s*(\d+)\s*\)$', value)
    if m:
        return {"path": m.group(1), "size": [int(m.group(2)), int(m.group(3))]}
    m = re.match(r'^Transform\(\s*"([^"\[]+)"\s*,\s*zoom\s*=\s*([\d.]+)\s*\)$', value)
    if m:
        return {"path": m.group(1), "zoom": float(m.group(2))}
    return None


def walk(line):
    for child in line.children:
        yield child
        if not child.text.startswith(("screen ", "python", "init ", "style ", "transform ", "layeredimage ")):
            yield from walk(child)


# ----------------------------------------------------------------------------
# 5. Put it together
# ----------------------------------------------------------------------------


def keep_only(ops, labels, order, wanted):
    """Keep just the chosen labels. Each one is cut off where the next label starts."""
    starts = sorted(labels[n] for n in order)
    new_ops, new_labels = [], {}
    for name in wanted:
        if name not in labels:
            sys.exit("label '%s' was not found" % name)
        start = labels[name]
        later = [s for s in starts if s > start]
        end = later[0] if later else len(ops)
        shift = len(new_ops) - start
        new_labels[name] = len(new_ops)
        for op in ops[start:end]:
            op = json.loads(json.dumps(op))
            if isinstance(op.get("to"), int):
                op["to"] = min(op["to"], end) + shift
            for choice in op.get("choices", []):
                choice["to"] += shift
            new_ops.append(op)
        new_ops.append({"t": "return"})
    return new_ops, new_labels


def resolve_asset(game_dir, path):
    for candidate in (path, "images/" + path, "audio/" + path):
        if os.path.isfile(os.path.join(game_dir, candidate)):
            return candidate
    return None


RENAMED = {}  # path in game/ -> path in the Godot project, for files with the wrong extension


def real_extension(path):
    """Look at the first bytes: a few .png files are really JPEGs. Ren'Py does not mind, Godot does."""
    with open(path, "rb") as f:
        head = f.read(12)
    if head.startswith(b"\x89PNG"):
        return ".png"
    if head.startswith(b"\xff\xd8"):
        return ".jpg"
    if head[:4] == b"RIFF" and head[8:12] == b"WEBP":
        return ".webp"
    return None


def copy_asset(game_dir, out_dir, rel):
    src = os.path.join(game_dir, rel)
    if not os.path.isfile(src):
        return False
    out_rel = rel
    stem, ext = os.path.splitext(rel)
    if ext.lower() in IMAGE_EXT:
        real = real_extension(src)
        same = real == ext.lower() or (real == ".jpg" and ext.lower() == ".jpeg")
        if real and not same:
            out_rel = stem + real
            RENAMED[rel] = out_rel
    dst = os.path.join(out_dir, "assets", "game", out_rel)
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    if not os.path.exists(dst) or os.path.getmtime(src) > os.path.getmtime(dst):
        shutil.copy2(src, dst)
    return True


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("game_dir", help="the Ren'Py game/ folder")
    ap.add_argument("godot_dir", help="the Godot project folder")
    ap.add_argument("--scripts", nargs="+", help="script files to convert (default: every script*.rpy)")
    ap.add_argument("--only", nargs="+", help="convert just these labels (handy for testing one scene)")
    args = ap.parse_args()
    if not args.scripts:
        args.scripts = sorted(n for n in os.listdir(args.game_dir)
                              if n.startswith("script") and n.endswith(".rpy"))

    report = []
    data = collect_game_data(args.game_dir, report)
    story_dir = os.path.join(args.godot_dir, "story")
    os.makedirs(story_dir, exist_ok=True)

    used_images, used_audio = set(), set()
    todo, skipped, python_blocks, screens = [], [], [], set()
    total_steps = 0
    for script in args.scripts:
        conv = Converter(data["characters"])
        conv.file = script
        conv.block(read_tree(os.path.join(args.game_dir, script)).children)
        ops, labels = conv.ops, conv.labels
        if args.only:
            wanted = [n for n in args.only if n in labels]
            if not wanted:
                continue
            ops, labels = keep_only(ops, labels, conv.label_order, wanted)
            kept = {op.get("line") for op in ops}
            conv.todo = [t for t in conv.todo if t[1] in kept]
            conv.skipped = [t for t in conv.skipped if t[1] in kept]
            conv.python_blocks = [t for t in conv.python_blocks if t[1] in kept]
            conv.screens = {op["name"] for op in ops if op["t"] == "screen"}
        if not labels:
            continue  # a setup-only file such as script.rpy's top half
        todo.extend(conv.todo)
        skipped.extend(conv.skipped)
        python_blocks.extend(conv.python_blocks)
        screens |= conv.screens
        total_steps += len(ops)

        for op in ops:
            if op["t"] in ("show", "scene") and op.get("image") and "text" not in op:
                used_images.add(op["image"])
            if op["t"] == "play":
                used_audio.add(op["file"])

        out = os.path.join(story_dir, os.path.splitext(script)[0] + ".json")
        with open(out, "w", encoding="utf-8") as f:
            json.dump({"source": script, "labels": labels, "ops": ops}, f, ensure_ascii=False, indent=1)
        print("wrote %s  (%d labels, %d steps, %d not converted)"
              % (out, len(labels), len(ops), len(conv.todo)))

    # Copy the art the converted story uses. `show kirako` with no expression can
    # mean any kirako picture, so every picture with a used tag (first word) is copied.
    missing = []
    used_tags = {name.split()[0] for name in used_images}
    for name in sorted(used_images):
        tag = name.split()[0]
        if name not in data["images"] and not (name == tag and any(k.split()[0] == tag for k in data["images"])):
            missing.append("picture '%s' is shown in the story but no file or `image` line matches it" % name)
    for name, entry in sorted(data["images"].items()):
        if entry.get("dynamic"):
            continue
        rel = resolve_asset(args.game_dir, entry["path"])
        if rel is None:
            if name.split()[0] in used_tags:
                missing.append("file for picture '%s' not found: %s" % (name, entry["path"]))
            continue
        entry["path"] = rel
        if name.split()[0] in used_tags:
            copy_asset(args.game_dir, args.godot_dir, rel)
    for audio in sorted(used_audio):
        rel = resolve_asset(args.game_dir, audio)
        if rel is None or not copy_asset(args.game_dir, args.godot_dir, rel):
            missing.append("audio file not found: %s" % audio)

    # Art used by the hand-built parts: dialogue box, choices, fonts, side picture, maps, bedroom, day display.
    always = [n for n in os.listdir(args.game_dir) if n.lower().endswith((".ttf", ".otf"))]
    for folder in ("gui", "gui/button", "gui/map", "images/side", "images/menu", "images/bedroom",
                   "images/cafe", "images/kirako", "gui/gallery", "gui/overlay", "gui/phone/overlay",
                   "images/naomi", "images/item", "images/wardrobe"):
        full = os.path.join(args.game_dir, folder)
        if os.path.isdir(full):
            always += [folder + "/" + n for n in os.listdir(full) if n.lower().endswith(IMAGE_EXT)]
    always += ["images/bg bedroom.png", "images/dept/counter_money.png", "images/speech.png",
               "images/back.png", "images/locked.png", "images/bg wardrobe.png"]
    # Pictures named in the gallery's `characters` table, and the gallery's cutscene pictures
    always += re.findall(r'"((?:images|gui)/[^"]+\.(?:png|jpg|jpeg|webp))"', data["defaults"].get("characters", ""))
    for button in data["gallery"]:
        for image in button["images"]:
            if image in data["images"]:
                always.append(data["images"][image]["path"])
    for rel in always:
        copy_asset(args.game_dir, args.godot_dir, rel)

    data["renamed"] = RENAMED
    with open(os.path.join(story_dir, "game_data.json"), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=1, sort_keys=True)

    with open(os.path.join(story_dir, "report.txt"), "w", encoding="utf-8") as f:
        f.write("Converted %d steps. %d were not converted.\n\n" % (total_steps, len(todo)))
        f.write("STORY LINES NOT CONVERTED (%d)\n" % len(todo))
        f.write("The player skips these and prints a warning. Port each one by hand.\n\n")
        for file, number, text, reason in todo:
            f.write("%s:%d  [%s]\n" % (file, number, reason))
            for row in text.split("\n"):
                f.write("    " + row + "\n")
            f.write("\n")
        f.write("\nPYTHON BLOCKS (%d)\n" % len(python_blocks))
        f.write("Each needs a function with this name in godot/state.gd.\n\n")
        for file, number, name, code in python_blocks:
            f.write("%s:%d  func %s()\n" % (file, number, name))
            for row in code.split("\n"):
                f.write("    " + row + "\n")
            f.write("\n")
        f.write("\nSCREENS THE STORY OPENS (%d)\n" % len(screens))
        f.write("Each needs a scene in godot/screens/. Until then a placeholder is shown.\n\n")
        for name in sorted(screens):
            f.write(name + "\n")
        f.write("\nEFFECTS LEFT OUT FOR NOW (%d)\n" % len(skipped))
        f.write("The picture shows, but without this effect (it needs a shader).\n\n")
        for file, number, what in skipped:
            f.write("%s:%d  %s\n" % (file, number, what))
        f.write("\nFILES WITH THE WRONG EXTENSION (%d)\n" % len(RENAMED))
        f.write("Copied into Godot under the right one. Worth renaming in game/ too.\n\n")
        for old, new in sorted(RENAMED.items()):
            f.write("%s is really a %s file\n" % (old, os.path.splitext(new)[1]))
        f.write("\nMISSING FILES (%d)\n\n" % len(missing))
        for row in missing:
            f.write(row + "\n")
        f.write("\nSETUP LINES THE CONVERTER DID NOT READ (%d)\n\n" % len(report))
        for row in report:
            f.write(row + "\n")
    print("wrote %s" % os.path.join(story_dir, "report.txt"))
    print("%d steps, %d not converted (%.1f%% converted)"
          % (total_steps, len(todo), 100.0 * (total_steps - len(todo)) / max(total_steps, 1)))


if __name__ == "__main__":
    main()
