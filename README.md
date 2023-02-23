# jittok

`jittok` is a Swiss Army Knife-like toolbox for data processing.

## Installation

```
pip install jittok
```

## Features

### `jptext` - Japanese text related functions

#### text normalization

```
>>> from jittok import jptext
>>> jptext.normalization("ｾﾞﾝｶｸｶﾅ")
'ゼンカクカナ'
```

#### parsing Japanese numeric string

```
>>> from jittok import jptext
>>> jptext.to_numeric("一二,三四五億2百十万987")
1234502100987
```
