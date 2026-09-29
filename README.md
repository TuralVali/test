# Two-Agent Python Dependency Explorer

This folder contains two VS Code GitHub Copilot custom agents and a standalone HTML preview.

## Agents

Place the two `.agent.md` files under:

```text
.github/agents/
```

### 1. Python Dependency Scanner

Use it to:

- analyze a Python module/function
- resolve internal dependencies
- classify external/builtin/unknown dependencies
- detect cycles
- capture source locations and snippets
- prepare the complete analysis for the report agent

### 2. Dependency HTML Report

Use it after the scanner to:

- create the interactive dependency graph
- add search/filter/layout controls
- provide node details
- provide source previews
- create the polished standalone HTML report

## Suggested Copilot workflow

```text
@Python Dependency Scanner

Analyze calculate_pd in src/models/pd_model.py.
Prepare the complete dependency analysis for the HTML report agent.
```

Then:

```text
@Dependency HTML Report

Using the dependency analysis from the previous agent,
generate the interactive HTML dependency report.
```

The final report should be created under:

```text
dependency_graphs/
```

## HTML preview

`dependency_graph_preview.html` is a visual preview/template showing the intended user interface.

The report agent should replace the demo graph with the actual scanned dependency graph.
