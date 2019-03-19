import pathlib
from typing import Dict, Any
import importlib.resources

import yamlutils

from . import api

ALIASES: Dict[str, Any]

def _load_aliases() -> None:
  global ALIASES
  data = importlib.resources.read_text('lilac2', 'aliases.yaml')
  ALIASES = yamlutils.load(data)

_load_aliases()

def load_lilac_yaml(dir: pathlib.Path) -> Dict[str, Any]:
  try:
    with open(dir / 'lilac.yaml') as f:
      conf = yamlutils.load(f)
  except FileNotFoundError:
    return {}

  update_on = conf.get('update_on')
  if update_on:
    for i, entry in enumerate(update_on):
      if isinstance(entry, str):
        update_on[i] = {entry: ''}
      elif 'alias' in entry.keys():
        update_on[i] = ALIASES[entry['alias']]

  if 'repo_depends' in conf:
    depends = conf.get('repo_depends')
  else:
    depends = conf.get('depends')
  if depends:
    for i, entry in enumerate(depends):
      if isinstance(entry, dict):
        depends[i] = next(iter(entry.items()))

  for func in ['pre_build', 'post_build', 'post_build_always']:
    name = conf.get(func)
    if name:
      funcvalue = getattr(api, name)
      conf[func] = funcvalue

  return conf
