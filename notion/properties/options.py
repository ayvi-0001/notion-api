# MIT License

# Copyright (c) 2023 ayvi-0001

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from enum import Enum
from typing import Sequence

__all__: Sequence[str] = (
    "CodeBlockLang",
    "BlockColor",
    "FunctionFormat",
    "NumberFormats",
    "PropertyColor",
)


class CodeBlockLang(str, Enum):
    abap = "abap"
    arduino = "arduino"
    bash = "bash"
    basic = "basic"
    c = "c"
    clojure = "clojure"
    coffeescript = "coffeescript"
    cplusplus = "c++"
    csharp = "c#"
    css = "css"
    dart = "dart"
    diff = "diff"
    docker = "docker"
    elixir = "elixir"
    elm = "elm"
    erlang = "erlang"
    flow = "flow"
    fortran = "fortran"
    fsharp = "f#"
    gherkin = "gherkin"
    glsl = "glsl"
    go = "go"
    graphql = "graphql"
    groovy = "groovy"
    haskell = "haskell"
    html = "html"
    java = "java"
    javascript = "javascript"
    json = "json"
    julia = "julia"
    kotlin = "kotlin"
    latex = "latex"
    less = "less"
    lisp = "lisp"
    livescript = "livescript"
    lua = "lua"
    makefile = "makefile"
    markdown = "markdown"
    markup = "markup"
    matlab = "matlab"
    mermaid = "mermaid"
    nix = "nix"
    objective_c = "objective-c"
    ocaml = "ocaml"
    pascal = "pascal"
    perl = "perl"
    php = "php"
    plain_text = "plain text"
    powershell = "powershell"
    prolog = "prolog"
    protobuf = "protobuf"
    python = "python"
    r = "r"
    reason = "reason"
    ruby = "ruby"
    rust = "rust"
    sass = "sass"
    scala = "scala"
    scheme = "scheme"
    scss = "scss"
    shell = "shell"
    sql = "sql"
    swift = "swift"
    typescript = "typescript"
    vb_net = "vb.net"
    verilog = "verilog"
    vhdl = "vhdl"
    visual_basic = "visual basic"
    webassembly = "webassembly"
    xml = "xml"
    yaml = "yaml"
    java_or_c = "java/c/c++/c#"


class FunctionFormat(str, Enum):
    average = "average"
    checked = "checked"
    count_ = "count"
    count_per_group = "count_per_group"
    count_values = "count_values"
    date_range = "date_range"
    earliest_date = "earliest_date"
    empty = "empty"
    latest_date = "latest_date"
    max = "max"
    median = "median"
    min = "min"
    not_empty = "not_empty"
    percent_checked = "percent_checked"
    percent_empty = "percent_empty"
    percent_not_empty = "percent_not_empty"
    percent_per_group = "percent_per_group"
    percent_unchecked = "percent_unchecked"
    range = "range"
    show_original = "show_original"
    show_unique = "show_unique"
    sum = "sum"
    unchecked = "unchecked"
    unique = "unique"


class NumberFormats(str, Enum):
    number = "number"
    number_with_commas = "number_with_commas"
    percent = "percent"
    dollar = "dollar"
    canadian_dollar = "canadian_dollar"
    euro = "euro"
    pound = "pound"
    yen = "yen"
    ruble = "ruble"
    rupee = "rupee"
    won = "won"
    yuan = "yuan"
    real = "real"
    lira = "lira"
    rupiah = "rupiah"
    franc = "franc"
    hong_kong_dollar = "hong_kong_dollar"
    new_zealand_dollar = "new_zealand_dollar"
    krona = "krona"
    norwegian_krone = "norwegian_krone"
    mexican_peso = "mexican_peso"
    rand = "rand"
    new_taiwan_dollar = "new_taiwan_dollar"
    danish_krone = "danish_krone"
    zloty = "zloty"
    baht = "baht"
    forint = "forint"
    koruna = "koruna"
    shekel = "shekel"
    chilean_peso = "chilean_peso"
    philippine_peso = "philippine_peso"
    dirham = "dirham"
    colombian_peso = "colombian_peso"
    riyal = "riyal"
    ringgit = "ringgit"
    leu = "leu"
    argentine_peso = "argentine_peso"
    uruguayan_peso = "uruguayan_peso"
    singapore_dollar = "singapore_dollar"


class BlockColor(str, Enum):
    default = "default"
    gray = "gray"
    brown = "brown"
    orange = "orange"
    yellow = "yellow"
    green = "green"
    blue = "blue"
    purple = "purple"
    pink = "pink"
    red = "red"
    gray_background = "gray_background"
    brown_background = "brown_background"
    orange_background = "orange_background"
    yellow_background = "yellow_background"
    green_background = "green_background"
    blue_background = "blue_background"
    purple_background = "purple_background"
    pink_background = "pink_background"
    red_background = "red_background"


class PropertyColor(str, Enum):
    """Color options for database property objects: select/multi_select/status."""

    default = "default"
    gray = "gray"
    brown = "brown"
    orange = "orange"
    red = "red"
    green = "green"
    blue = "blue"
    purple = "purple"
    pink = "pink"
    yellow = "yellow"
