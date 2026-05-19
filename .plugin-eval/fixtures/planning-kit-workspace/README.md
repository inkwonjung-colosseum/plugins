# planning-kit benchmark fixture

Small workspace used by plugin-eval benchmarks for `planning-kit`.

Keep this fixture intentionally small. The benchmark installs the plugin under
`plugins/planning-kit`, so scenarios should read the installed plugin contract
from there and write temporary planning outputs under this fixture workspace.
