# Framework Detection Reference

Probe order for language-agnostic test framework detection:

## 1. Python
| File | Test Framework | Command |
|------|---------------|---------|
| `pyproject.toml` (contains `[tool.pytest]`) | pytest | `uv run pytest` or `python -m pytest` |
| `pyproject.toml` (contains `[tool.unittest]`) | unittest | `python -m unittest discover` |
| `setup.cfg` (contains `[tool:pytest]`) | pytest | `pytest` |
| `tox.ini` | tox | `tox` |
| `noxfile.py` | nox | `nox` |

## 2. Node.js / JavaScript / TypeScript
| File | Test Framework | Command |
|------|---------------|---------|
| `package.json` → `scripts.test` | Any | `npm test` or `yarn test` |
| `jest.config.js` | Jest | `npx jest` |
| `vitest.config.ts` | Vitest | `npx vitest run` |
| `mocha.opts` or `.mocharc.js` | Mocha | `npx mocha` |
| `playwright.config.ts` | Playwright | `npx playwright test` |

## 3. Rust
| File | Test Framework | Command |
|------|---------------|---------|
| `Cargo.toml` | cargo test | `cargo test` |

## 4. Go
| File | Test Framework | Command |
|------|---------------|---------|
| `go.mod` | go test | `go test ./...` |

## 5. Ruby
| File | Test Framework | Command |
|------|---------------|---------|
| `Gemfile` + `spec/` | RSpec | `bundle exec rspec` |
| `Gemfile` + `test/` | Minitest | `bundle exec ruby -Itest` |

## 6. Java / JVM
| File | Test Framework | Command |
|------|---------------|---------|
| `build.gradle` or `build.gradle.kts` | Gradle | `./gradlew test` |
| `pom.xml` | Maven | `mvn test` |
| `pom.xml` + surefire config | JUnit | `mvn test` |

## 7. Elixir
| File | Test Framework | Command |
|------|---------------|---------|
| `mix.exs` | ExUnit | `mix test` |

## 8. Fallback
- `Makefile` → `make test`
- `CMakeLists.txt` → `cmake --build . && ctest`
- None detected → ask user
