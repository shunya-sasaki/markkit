# markkit

A formatter for math blocks in Markdown files.

`markkit` rewrites every math block in a Markdown file to a single,
consistent style: either `$$` dollar blocks or ` ```math ` code blocks.
Indentation of each block is preserved.

## 📦 Requirements

- Python >= 3.11

## ⚙️ Setup

We recommend installing `markkit` with [uv](https://docs.astral.sh/uv/).
It installs the package into an isolated environment and puts the `mk`
command on your `PATH`:

```sh
uv tool install git+https://github.com/shunya-sasaki/markkit.git
```

## 🚀 Usage

Format a Markdown file in place:

```sh
mk fmt path/to/file.md
```

Choose the output style with `--math-block-type` / `-m`
(`dollar` by default):

```sh
mk fmt path/to/file.md -m code-block
```

Print the result instead of writing to the file with `--no-write`:

```sh
mk fmt path/to/file.md --no-write
```

### Options

| Option                   | Values                | Default  | Description                             |
| ------------------------ | --------------------- | -------- | --------------------------------------- |
| `--math-block-type`, `-m`| `dollar`, `code-block`| `dollar` | Output style for math blocks.           |
| `--write`                | flag                  | `True`   | Write the result back to the file.      |
| `--no-write`             | flag                  | –        | Print the result instead of writing it. |

## 📄 License

MIT License

See [LICENSE](./LICENSE) for the detail.

