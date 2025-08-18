to_entries[] | select(.key as $k | $k | IN($names[])) |
  [
    ("`" + .key + " <" + .value.url + ">`__"),
    (.value.clinical.tags // [] | join(" ")),
     (.value.clinical.olives // [] | map("`" + . + " <https://bitbucket.oicr.on.ca/projects/GSI/repos/analysis-config/browse/shesmu/production-cap/" + . + ">`__") | join(" ")),
    (.value.data_modules // [] | join(" ")),
    (.value.code_modules // [] | join(" "))
  ] | @csv
