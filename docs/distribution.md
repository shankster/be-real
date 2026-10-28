# Distribution and validation

## Current validation status

Preparation run on macOS, 2026-10-28:

- Storage tests passed under Python 3.12.7, including concurrent writers, revision conflicts, interrupted writes, Unicode names and paths, UTF-8 BOM input, and lock release after process termination.
- Platform-directory selection was exercised for macOS, Linux/XDG, and Windows/LOCALAPPDATA, including overrides and missing or relative environment values.
- The Windows locking API contract was exercised with a test double. This is not a native Windows run.
- Skills CLI 1.7.4 installed the full bundle independently for Claude Code, Codex, Cursor, GitHub Copilot, Gemini CLI, OpenCode, Cline, and Windsurf in temporary projects. Installed helpers ran and reused one temporary store. Telemetry was disabled; personal installations and records were not used.
- The GitHub Actions run for commit `641bf6f` passed native storage and installation checks on Ubuntu and Windows, and the installation check on macOS. The configured workflow now tests Python 3.10 and 3.14 on Ubuntu and Windows, plus the eight-target installer on each; run the same checks locally on macOS.
- Live model behavior across these agents has not been evaluated. Installation success does not demonstrate good assessment judgment; use the behavioral cases below before advertising verified agent behavior.

The package uses standard Agent Skills frontmatter and relative references. Optional Codex UI metadata has no role in storage or assessment correctness. The license travels with the installed folder.

## Reproduce

From the repository root, using Python 3.10+:

```sh
python3 -B -m unittest discover -s tests -v
python3 -B tools/test_install.py
```

Use `py -3` or `python` on Windows. The installation check requires Node.js 22.20+ and network access to npm; the offline test suite does not. It pins the installer version so a CLI change does not silently change the validation baseline. Update the pin deliberately and rerun the installation check when adopting a newer version.

Run [behavioral cases](../tests/behavioral-cases.md) in the agents being evaluated. Record agent/model version, date, tool access, actual output, and pass/fail observations. Do not mark a target behavior-tested based only on bundle discovery or a mocked tool.

## Prepare a public release

1. Review the diff and include `skills/`, `tests/`, `tools/`, `docs/`, `.github/`, `.gitignore`, `.gitattributes`, README, and LICENSE in the release commit. Keep personal assessment records outside the repository. The bundled skill needs its references, helper, metadata, and license together.
2. Push the reviewed commit to the intended public branch of `shankster/be-real`. Publishing is a separate action from local preparation.
3. Run the macOS checks locally and wait for native storage and installation CI on Ubuntu and Windows. Resolve failures and publish the actual compatibility results.
4. Verify remote discovery with `npx skills add shankster/be-real --list`, then install from GitHub into a clean project. The local smoke test cannot prove that the remote branch contains the same files.
5. Tag the reviewed version, for example `v0.1.0`, and include tested environments and known limits in its release notes. This guide does not imply a tag or release already exists.
6. Share `npx skills add shankster/be-real --skill be-real -g`. Remove the README's pre-publication qualifier once the remote installation is verified.

According to the [Skills.sh FAQ](https://skills.sh/docs/faq), skills are hosted in GitHub repositories and leaderboard inclusion follows installation telemetry. There is no separate npm package or custom installer to publish for this layout. Do not claim listing or manufacture installs from local tests; our test runner disables telemetry. Users control their own telemetry preferences.

The [Skills CLI documentation](https://github.com/vercel-labs/skills/blob/main/docs/commands.md) describes installation, agent selection, copy mode, and updates. The [Agent Skills specification](https://agentskills.io/specification) defines the shared bundle format.
