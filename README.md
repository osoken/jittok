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

### `jpdatetime` - Japanese datetime related functions

#### parsing Japanese "wareki" string

```
>>> from jittok import jpdatetime
>>> jpdatetime.strptime("令和元年10月3日", "%Y年%m月%d日")
datetime.datetime(2019, 10, 3, 0, 0)
>>> jpdatetime.strptime("昭和64年1月1日", "%Y年%m月%d日")
datetime.datetime(1989, 1, 1, 0, 0)
```

It parses `"明治"`, `"大正"`, `"昭和"`, `"平成"`, `"令和"` and does not support consistency check:

```
>>> from jittok import jpdatetime
>>> jpdatetime.strptime("大正90年10月3日", "%Y年%m月%d日")
datetime.datetime(2001, 10, 3, 0, 0)
```
