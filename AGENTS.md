# AGENTS.md

# Python Dependency Graph Visualizer
## VS Code + GitHub Copilot Agent Instructions

---

## 1. Purpose

Build a Python dependency-analysis and visualization tool that can be used directly from VS Code with GitHub Copilot Agent mode.

The tool must accept:

- A Python module/file
- A Python function
- Optional class name
- Optional dependency depth

It must analyze the Python source code statically and generate an interactive HTML visualization showing the dependency tree/call graph.

The primary output is an HTML file that can be opened directly in a browser.

Example:

```text
Input:
    src/models/pd_model.py
    calculate_pd

Output:
    dependency_graph.html
```

The HTML visualization should be professional, interactive, and easy to understand.

---

## 2. Primary User Experience

The intended workflow is:

```text
VS Code
   │
   ▼
GitHub Copilot Agent
   │
   ├── User provides Python file
   ├── User provides function name
   │
   ▼
Static Python Analysis
   │
   ├── Parse AST
   ├── Find target function
   ├── Find function calls
   ├── Resolve dependencies
   ├── Traverse dependency graph
   ├── Detect circular dependencies
   │
   ▼
Graph Builder
   │
   ▼
Interactive HTML
```

The user should not need to manually construct the dependency tree.

---

## 3. Example User Request

The agent should understand requests such as:

```text
Analyze:

src/models/pd_model.py

Function:

calculate_pd

Generate an interactive HTML dependency graph.
```

Or:

```text
Create a dependency graph for calculate_pd in
src/models/pd_model.py
with maximum depth 8.
```

Or:

```text
Analyze calculate_pd and generate the dependency visualization.
```

The agent should infer reasonable defaults.

---

## 4. Default Behavior

If the user does not specify options, use:

```text
direction        = downstream
max_depth        = 10
output           = HTML
include_external = true
include_builtin  = false
open_browser     = false
```

The target function must be highlighted clearly.

---

## 5. Dependency Direction

Support two graph directions.

### Downstream

Show what the selected function depends on.

Example:

```text
calculate_pd
      │
      ├──────────────┐
      ▼              ▼
prepare_features  calculate_score
                       │
                       ▼
                  calculate_mean
```

This should be the default.

### Upstream

Show what functions depend on the selected function.

Example:

```text
run_icaap
     │
     ▼
build_model
     │
     ▼
calculate_pd
```

Support:

```text
--direction downstream
```

and:

```text
--direction upstream
```

---

## 6. Static Analysis

The dependency analyzer must primarily use Python AST.

Use:

```python
import ast
```

Do NOT execute arbitrary user code simply to determine dependencies.

The analyzer should inspect:

- FunctionDef
- AsyncFunctionDef
- ClassDef
- Import
- ImportFrom
- Call
- Attribute
- Name
- Lambda

---

## 7. What Must Be Detected

Detect:

### Functions

```python
calculate_pd()
```

### Methods

```python
self.calculate_pd()
```

### Imported functions

```python
from calibration import calibrate

calibrate()
```

### Module functions

```python
import calibration

calibration.calibrate()
```

### Class methods

```python
model.calculate_pd()
```

### Nested functions

```python
def outer():

    def inner():
        ...
```

### Decorated functions

```python
@staticmethod
def calculate_pd():
    ...
```

### Async functions

```python
async def calculate_pd():
    ...
```

---

## 8. Dependency Classification

Every dependency should be classified as one of:

```text
INTERNAL
EXTERNAL
BUILTIN
UNKNOWN
```

Example:

```text
calculate_pd
│
├── validate_input       INTERNAL
├── prepare_features     INTERNAL
├── numpy.exp             EXTERNAL
├── pandas.DataFrame      EXTERNAL
└── len                   BUILTIN
```

---

## 9. Internal Dependency Resolution

The resolver should attempt to identify the actual source definition.

Resolution priority:

1. Same function/module
2. Same class
3. Imported function
4. Imported local module
5. Another Python file in the project
6. Installed third-party package
7. Python builtin
8. Unknown

Do not falsely claim that an unresolved dependency was resolved.

Use:

```text
UNKNOWN
```

when resolution cannot be established reliably.

---

## 10. Project Root

Determine the project root.

Prefer the Git repository root when a `.git` directory exists.

If no Git repository exists, use the nearest workspace/project root.

Resolve local imports relative to the project.

Skip unrelated directories by default:

```text
.git/
.venv/
venv/
__pycache__/
node_modules/
dist/
build/
```

---

## 11. Circular Dependencies

Circular dependencies must be detected.

Example:

```text
calculate_pd
    │
    ▼
calculate_score
    │
    ▼
validate_score
    │
    ▼
calculate_pd
```

The HTML graph must visually indicate the cycle.

Example node label:

```text
calculate_pd
[CIRCULAR]
```

Do not recursively traverse a cycle forever.

---

## 12. Maximum Depth

Support:

```text
--max-depth
```

Default:

```text
10
```

Example:

```bash
python dependency_graph.py \
    --module src/models/pd_model.py \
    --function calculate_pd \
    --max-depth 8
```

If the maximum depth is reached, display:

```text
MAX DEPTH
```

or an ellipsis node.

---

## 13. HTML Output

The main output MUST be HTML.

Example:

```text
dependency_graph.html
```

The HTML should be self-contained whenever possible.

The user should be able to open the file without starting a Python web server.

Avoid requiring external services.

Prefer embedding required JavaScript/CSS into the HTML.

---

## 14. Graph Visualization

The graph should look professional and interactive.

Recommended technology:

```text
Cytoscape.js
```

or another mature JavaScript graph visualization library.

The generated graph should support:

- Zoom
- Pan
- Drag nodes
- Node selection
- Highlighting
- Search
- Fit graph to screen
- Reset graph
- Collapse/expand where practical
- Hover information
- Click information
- Different node styles
- Different edge styles
- Legend

If Cytoscape.js is used, prefer bundling or embedding the required library so the HTML can work offline.

---

## 15. Graph Layout

Use a hierarchical layout appropriate for directed dependency graphs.

Preferred algorithms:

```text
dagre
breadthfirst
elk
```

Default to `dagre` if available.

---

## 16. Visual Design

The HTML should have a modern developer-tool appearance.

Include:

```text
┌─────────────────────────────────────────────────────────┐
│ Python Dependency Graph                                 │
│                                                         │
│ File: src/models/pd_model.py                            │
│ Function: calculate_pd                                  │
│ Dependencies: 14                                        │
│                                                         │
│ [Search] [Fit] [Reset] [Collapse] [Expand]             │
├─────────────────────────────────────────────────────────┤
│                                                         │
│                    calculate_pd                         │
│                         │                               │
│              ┌──────────┼──────────┐                   │
│              ▼          ▼          ▼                   │
│        validate()   prepare()   calibrate()            │
│             │          │                               │
│             ▼          ▼                               │
│          checks()   transform()                        │
│                                                         │
├─────────────────────────────────────────────────────────┤
│ Legend                                                  │
│ ● Internal  ● External  ● Builtin  ● Unknown           │
└─────────────────────────────────────────────────────────┘
```

Use centralized CSS variables/configuration for semantic node styles rather than scattering hard-coded colors throughout the application.

---

## 17. Node Information

Every node should contain metadata.

Example:

```json
{
  "id": "calculate_pd",
  "name": "calculate_pd",
  "type": "function",
  "dependency_type": "internal",
  "file": "src/models/pd_model.py",
  "line": 42,
  "column": 1,
  "depth": 0
}
```

For external dependencies:

```json
{
  "name": "numpy.exp",
  "dependency_type": "external"
}
```

---

## 18. Node Click Behavior

When a user clicks a node, display a details panel.

Example:

```text
Function
--------------------------------
calculate_score

Type
--------------------------------
Function

Dependency
--------------------------------
INTERNAL

File
--------------------------------
src/models/pd_model.py

Line
--------------------------------
87

Depth
--------------------------------
1

Dependencies
--------------------------------
3
```

For external dependencies:

```text
Module
--------------------------------
numpy

Function
--------------------------------
exp

Type
--------------------------------
EXTERNAL
```

---

## 19. Source Code Preview

If practical, clicking an internal node should display a source-code preview.

Example:

```text
src/models/pd_model.py:87

def calculate_score(df):
    score = df["score"].mean()
    return score
```

Do not execute the source code.

The preview can be embedded in the HTML.

---

## 20. Search

The HTML should include a search box:

```text
Search dependency...
```

Typing:

```text
calibrate
```

should highlight matching nodes such as:

```text
calibrate_pd
calibrate_score
calibrate_model
```

---

## 21. Hover Behavior

Hovering over a node should show a tooltip containing:

- Name
- File
- Line
- Type
- Dependency type
- Depth

Example:

```text
calculate_score

src/models/pd_model.py:87

INTERNAL
Depth: 1
```

---

## 22. Graph Controls

Provide buttons for:

```text
Fit
Reset
Zoom In
Zoom Out
Search
Expand All
Collapse All
Download
```

Where practical.

---

## 23. Download

Allow the user to download/export:

- HTML
- JSON
- SVG
- PNG

If implementation complexity is high, HTML and JSON are mandatory.

---

## 24. Legend

The HTML must include a legend.

Example:

```text
Legend

● Target function
● Internal function
● External dependency
● Builtin
● Unknown
⚠ Circular dependency
```

---

## 25. Statistics Panel

Display summary statistics.

Example:

```text
Dependency Analysis

Target:
calculate_pd

Total nodes:
18

Internal:
12

External:
4

Builtin:
2

Unknown:
0

Maximum depth:
5

Circular dependencies:
1
```

---

## 26. Function Signature

Show function signatures.

Example:

```text
calculate_pd(
    df: pd.DataFrame,
    macro_data: pd.DataFrame
) -> pd.Series
```

If type hints are unavailable, display the available signature information.

---

## 27. CLI

Implement:

```bash
python dependency_graph.py \
    --module <path> \
    --function <function>
```

Optional:

```text
--class <class>
--direction downstream|upstream
--max-depth <N>
--max-nodes <N>
--output <path>
--format html|json
--include-external
--include-builtins
--internal-only
```

Example:

```bash
python dependency_graph.py \
    --module src/models/pd_model.py \
    --function calculate_pd \
    --direction downstream \
    --max-depth 8 \
    --output dependency_graph.html
```

---

## 28. Recommended Project Structure

Create the following structure:

```text
python_dependency_visualizer/
│
├── dependency_graph.py
│
├── analyzer/
│   ├── __init__.py
│   ├── ast_parser.py
│   ├── resolver.py
│   ├── analyzer.py
│   └── models.py
│
├── visualization/
│   ├── __init__.py
│   ├── html_generator.py
│   ├── graph_builder.py
│   └── templates/
│       └── dependency_graph.html
│
├── cli/
│   ├── __init__.py
│   └── arguments.py
│
├── tests/
│   ├── test_ast_parser.py
│   ├── test_resolver.py
│   ├── test_analyzer.py
│   └── test_html_generator.py
│
├── requirements.txt
└── README.md
```

Keep analysis, resolution, graph building, visualization, and CLI concerns separated.

---

## 29. Data Model

Use dataclasses.

Example:

```python
@dataclass
class DependencyNode:
    id: str
    name: str
    node_type: str
    dependency_type: str
    file: str | None
    line: int | None
    column: int | None
    depth: int
    signature: str | None = None
    source: str | None = None
    circular: bool = False
```

Edge:

```python
@dataclass
class DependencyEdge:
    source: str
    target: str
    edge_type: str
```

Graph:

```python
@dataclass
class DependencyGraph:
    nodes: list[DependencyNode]
    edges: list[DependencyEdge]
    root: str
```

---

## 30. AST Parser

`ast_parser.py` should be responsible only for static source analysis.

It should identify:

- FunctionDef
- AsyncFunctionDef
- ClassDef
- Import
- ImportFrom
- Call
- Attribute
- Name
- Lambda

Extract:

- function name
- class name
- parameters
- return annotation
- decorators
- line
- column
- source
- calls
- imports

Do not mix visualization logic into the AST parser.

---

## 31. Resolver

The resolver converts an AST call into a dependency node.

Examples:

```python
calculate_score()
```

becomes:

```text
calculate_score
```

and:

```python
utils.calculate_score()
```

becomes:

```text
utils.calculate_score
```

Attempt to resolve local definitions to their actual file and line.

---

## 32. Handling Pandas / NumPy / Scikit-learn

The analyzer must not attempt to recursively analyze every implementation detail of external packages.

For example:

```python
df.groupby("rating").mean()
```

should normally appear as an external dependency rather than expanding the complete pandas implementation.

Similarly:

```python
np.exp(x)
```

should appear as:

```text
numpy.exp
```

rather than traversing NumPy internals.

This is important for large data-science and risk-modeling projects.

---

## 33. Dependency Filtering

Allow users to filter dependency types.

For example:

```text
Internal only
```

should show:

```text
calculate_pd
├── validate_input
├── prepare_features
└── calibrate
```

while hiding external dependencies.

Support:

```bash
--internal-only
```

---

## 34. Repository Mode

Design the code so that it can later support:

```bash
python dependency_graph.py \
    --repo . \
    --function calculate_pd
```

The initial implementation may focus on:

```text
--module
--function
```

but the architecture must support repository-wide analysis later.

---

## 35. Git Integration

Keep the architecture ready for future Git integration.

Do not implement Git comparison unless requested.

Future concept:

```text
Commit A
    ↓
Dependency Graph A

Commit B
    ↓
Dependency Graph B

        ↓

Dependency Changes
```

Potential future output:

```text
ADDED
+ validate_monotonicity()

REMOVED
- old_calibration()

CHANGED
~ calculate_score()

UNCHANGED
  prepare_features()
```

---

## 36. Future Impact Analysis

The architecture should eventually support:

```text
"If I change this function, what functions may be affected?"
```

The graph model should therefore support both:

```text
caller -> callee
```

and reverse lookup:

```text
callee -> callers
```

---

## 37. HTML Template

The generated HTML should contain:

```html
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">

    <title>Python Dependency Graph</title>

    <style>
        /* Application styles */
    </style>
</head>

<body>

    <header>
        <!-- title and metadata -->
    </header>

    <main>

        <aside>
            <!-- controls -->
            <!-- search -->
            <!-- statistics -->
            <!-- legend -->
        </aside>

        <section id="graph">
            <!-- Cytoscape graph -->
        </section>

        <aside id="details">
            <!-- node details -->
        </aside>

    </main>

    <script>
        // graph visualization
    </script>

</body>
</html>
```

---

## 38. Responsive Layout

The HTML should work on:

- Desktop
- Laptop
- VS Code browser preview
- Normal web browser

Minimum recommended resolution:

```text
1280 x 720
```

The graph should use the available viewport.

---

## 39. Large Graph Handling

Some Python projects may contain hundreds or thousands of dependencies.

Do not render an unlimited graph by default.

Use:

```text
max_depth
max_nodes
```

Default:

```text
max_nodes = 500
```

If the graph exceeds the limit:

```text
Graph truncated.

500 nodes displayed.

Increase --max-nodes to inspect more dependencies.
```

---

## 40. Error Handling

Handle:

### File does not exist

```text
ERROR:
Python module does not exist:
src/models/pd_model.py
```

### Function does not exist

```text
ERROR:
Function 'calculate_pd' was not found.
```

### Invalid Python

```text
ERROR:
Unable to parse Python file.

Line:
42

Reason:
invalid syntax
```

### Ambiguous function

If multiple functions have the same name:

```text
WARNING:
Multiple functions named calculate_score were found.

Specify:

--class <class_name>
```

---

## 41. Testing

Use:

```text
pytest
```

Tests must cover:

1. Simple dependency
2. Multiple dependencies
3. Recursive dependencies
4. Imported functions
5. Local modules
6. External modules
7. Builtins
8. Class methods
9. `self.method()`
10. Nested functions
11. Circular dependencies
12. Maximum depth
13. Missing functions
14. Invalid syntax
15. HTML generation
16. JSON generation
17. Search metadata
18. Graph statistics

---

## 42. Example Python Input

Given:

```python
from features import prepare_features
from calibration import calibrate
import numpy as np


def calculate_pd(df):

    df = prepare_features(df)

    score = calculate_score(df)

    pd_value = calibrate(score)

    return np.exp(pd_value)


def calculate_score(df):

    return df["score"].mean()
```

The resulting graph should approximately be:

```text
                    ┌──────────────────────┐
                    │    calculate_pd      │
                    │       TARGET         │
                    └──────────┬───────────┘
                               │
              ┌────────────────┼────────────────┐
              │                │                │
              ▼                ▼                ▼
     prepare_features   calculate_score     calibrate
              │                │
              ▼                ▼
        features.py     pandas.DataFrame
                            .mean()

                         numpy.exp
```

---

## 43. HTML User Experience

When the HTML is opened, the user should immediately see:

```text
┌─────────────────────────────────────────────────────────────┐
│ PYTHON DEPENDENCY GRAPH                                     │
│                                                             │
│ calculate_pd                                                │
│ pd_model.py                                                 │
│                                                             │
│ 18 Nodes     17 Edges     Depth 5     12 Internal          │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  [ Search dependencies... ]                                 │
│                                                             │
│  [Fit] [Reset] [Expand] [Collapse] [Download]              │
│                                                             │
│                  ┌───────────────┐                          │
│                  │ calculate_pd  │                          │
│                  │    TARGET     │                          │
│                  └───────┬───────┘                          │
│                          │                                  │
│             ┌────────────┼────────────┐                     │
│             ▼            ▼            ▼                     │
│        prepare()     score()      calibrate()               │
│             │            │                                  │
│             ▼            ▼                                  │
│        transform()   pandas.mean()                          │
│                                                             │
├─────────────────────────────────────────────────────────────┤
│ Details                                                     │
│                                                             │
│ Function: calculate_score                                   │
│ Type: INTERNAL                                              │
│ File: src/models/pd_model.py                               │
│ Line: 15                                                    │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 44. VS Code Integration

The project must work naturally with VS Code.

The user should be able to ask GitHub Copilot Agent:

```text
Analyze the function calculate_pd in:

src/models/pd_model.py

Generate the interactive HTML dependency graph.
```

Copilot should:

1. Inspect the project.
2. Find the analyzer.
3. Run the analyzer.
4. Generate the HTML.
5. Report the generated file path.
6. If supported by the environment, offer/open the HTML in a browser.

Example response:

```text
Dependency analysis completed.

Function:
calculate_pd

Nodes:
24

Edges:
31

Internal dependencies:
17

External dependencies:
6

Builtins:
1

Unknown:
0

Maximum depth:
6

HTML generated:

reports/calculate_pd_dependency_graph.html
```

---

## 45. Copilot Agent Behavior

When modifying this project, GitHub Copilot Agent must:

- Inspect existing implementation before creating new files.
- Reuse existing utilities where possible.
- Avoid unnecessary dependencies.
- Keep analysis separate from visualization.
- Add tests for new functionality.
- Preserve existing functionality.
- Run tests after modifications.
- Report test results.
- Never silently remove functionality.
- Never execute arbitrary project code just to discover dependencies.

---

## 46. When User Provides Only a Function

If the user says:

```text
Analyze calculate_pd
```

Copilot should search the current workspace for the function.

If exactly one definition is found, use it.

If multiple definitions are found, ask the user to specify the module/class.

Example:

```text
I found 3 definitions of calculate_pd:

1. src/models/pd_model.py
2. tests/test_pd.py
3. legacy/pd_model.py

Which one should I analyze?
```

---

## 47. When User Provides a Folder

If the user provides:

```text
src/models/
```

the agent should:

1. Search all `.py` files.
2. Identify the requested function.
3. Analyze local dependencies.
4. Generate the graph.

Do not modify Python source files unless explicitly requested.

---

## 48. Output Location

Default output:

```text
dependency_graphs/
```

Example:

```text
dependency_graphs/
└── calculate_pd_dependency_graph.html
```

For multiple functions:

```text
dependency_graphs/
├── calculate_pd_dependency_graph.html
├── calculate_lgd_dependency_graph.html
└── calculate_ead_dependency_graph.html
```

Create the directory if it does not exist.

---

## 49. Naming

Use:

```text
<function_name>_dependency_graph.html
```

Example:

```text
calculate_pd_dependency_graph.html
```

If duplicate names exist:

```text
pd_model_calculate_pd_dependency_graph.html
```

---

## 50. JSON Export

Alongside HTML, optionally generate:

```text
calculate_pd_dependency_graph.json
```

Example:

```json
{
    "root": "calculate_pd",
    "nodes": [],
    "edges": [],
    "statistics": {
        "total_nodes": 18,
        "internal": 12,
        "external": 4,
        "builtin": 2,
        "unknown": 0,
        "max_depth": 5,
        "circular_dependencies": 1
    }
}
```

The JSON should make the graph reusable by other tools.

---

## 51. No False Dependencies

Accuracy is more important than completeness.

If the analyzer cannot confidently resolve:

```python
obj.calculate()
```

do not assume what `obj` is.

Instead display:

```text
obj.calculate()
[UNKNOWN]
```

This is preferable to inventing a dependency.

---

## 52. Performance

The analyzer should avoid repeatedly parsing the same files.

Implement caching where appropriate.

For example:

```text
file -> parsed AST
```

should be cached during a single analysis.

For large repositories, avoid scanning unrelated directories.

---

## 53. Security

Never:

- Execute arbitrary Python source
- Run unknown functions
- Import project modules just to inspect them
- Execute shell commands from analyzed source
- Modify source files during analysis

Static analysis is the default.

---

## 54. Documentation

Create a README explaining:

1. Installation
2. Usage
3. CLI options
4. Examples
5. HTML output
6. Supported dependency types
7. Known limitations
8. Troubleshooting
9. VS Code + GitHub Copilot usage

Example:

```bash
python dependency_graph.py \
    --module src/models/pd_model.py \
    --function calculate_pd
```

---

## 55. Acceptance Criteria

The implementation is complete only when all of the following are true:

### Analysis

- [ ] Python AST is parsed.
- [ ] Target function is identified.
- [ ] Direct dependencies are identified.
- [ ] Recursive dependencies are identified.
- [ ] Internal dependencies are resolved.
- [ ] External dependencies are identified.
- [ ] Builtins can be identified.
- [ ] Unknown dependencies are marked.
- [ ] Circular dependencies are detected.
- [ ] Maximum depth is respected.

### Visualization

- [ ] HTML is generated.
- [ ] Graph is interactive.
- [ ] Nodes can be dragged.
- [ ] Graph can be zoomed.
- [ ] Graph can be panned.
- [ ] Graph can be fitted to screen.
- [ ] Nodes can be searched.
- [ ] Node details are displayed.
- [ ] Target function is clearly highlighted.
- [ ] Internal/external/builtin/unknown dependencies are visually distinguishable.
- [ ] Legend exists.
- [ ] Statistics exist.

### VS Code

- [ ] Works from VS Code terminal.
- [ ] Works with GitHub Copilot Agent.
- [ ] Output path is clearly reported.
- [ ] Does not require manual graph construction.
- [ ] Does not modify source code during analysis.

### Quality

- [ ] Unit tests exist.
- [ ] Tests pass.
- [ ] Type hints are used.
- [ ] Code is modular.
- [ ] Errors are handled gracefully.
- [ ] No arbitrary source execution is required.

---

## 56. Future Git Comparison Mode

Keep the architecture ready for a future command:

```bash
python dependency_graph.py \
    --module src/models/pd_model.py \
    --function calculate_pd \
    --commit-before abc123 \
    --commit-after def456
```

Future visualization:

```text
BEFORE                         AFTER

calculate_pd                  calculate_pd
     │                              │
     ├── validate()                 ├── validate()
     ├── score()                    ├── score()
     └── calibrate()                ├── validate_monotonicity()
                                    └── calibrate()
```

The future HTML should be able to highlight:

```text
ADDED
REMOVED
CHANGED
UNCHANGED
```

Do not implement Git comparison until explicitly requested.

---

## 57. Final Agent Instruction

When the user asks for a dependency graph:

1. Identify the Python module.
2. Identify the target function.
3. Determine the project root.
4. Parse the relevant Python source.
5. Resolve dependencies statically.
6. Build the dependency graph.
7. Detect cycles.
8. Apply depth/node limits.
9. Generate the interactive HTML.
10. Generate JSON if requested or useful.
11. Validate that the HTML was successfully created.
12. Run tests when code was changed.
13. Report the output location and key statistics.

The primary deliverable is always:

```text
Interactive HTML dependency graph
```

The graph must be visually useful, not merely a text representation of the dependency tree.
