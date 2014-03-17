判例要旨抜き出しスクリプト
--------------------------

概要
~~~~
https://github.com/drowse314-dev-ymat/hanrei_getter からダウンロードした判例のXMLファイルから、要旨のテキストを抜き出します。

使い方
~~~~~~
事前に必要なのは、Python2.7およびvirtualenvのみです。

`こちら <https://github.com/drowse314-dev-ymat/hanrei_getter>`_ で得られるフォーマットのXMLファイルに対応しています。
要旨の抽出は、このXMLファイルの蓄積されたディレクトリをひとつ指定して行います。

.. code-block::

    hanrei_collection
    ├── minji_joukoku_1.xml
    ├── minji_joukoku_2.xml
    └── minji_kyokakoukoku_1.xml

それぞれのXMLファイル名は、 ``<any text>_<category>_<any text>.xml`` のように2つ以上のアンダーラインを含む必要があります。
``<category>`` の部分文字列は要旨の出力ディレクトリを分けるために使われるため、カテゴリ分けとして有用なものを使うようにします。

出力先ディレクトリ ``target_dir`` を決め、

.. code-block:: sh

    $ cd hanrei_abstract_extractor
    $ virtualenv-2.7 venv # 名前はなんでも
    $ source venv/bin/activate
    $ pip install -r requirements.txt
    $ sh ex_abst.sh hanrei_collection target_dir

とします。 ``target_dir`` が存在しなければ、勝手に作成します。

これにより判例要旨は、 ``target_dir`` 下に各判例のカテゴリに従って作成されたサブディレクトリ
``target_dir/<category>`` 下にテキストとして蓄積されます。

.. code-block::

    target_dir
    ├── joukoku
    │   ├── joukoku.h7.6.23.1.txt
    │   └── joukoku.s62.4.4.1.txt
    └── kyokakoukoku
        └── kyokakoukoku.h9.1.1.1.txt

一判例につき一ファイルが作成され、ファイル名は ``<category>.<日本の年号 + #year>.<#month>.<#day>.<#同日の判例の通し番号>.txt``
となります。

なお、要旨の付与されていない判例( ``<Hanrei />`` 下の ``<Abstract />`` の中のテキストが空欄のもの)は無視されます
(要旨のファイルが作成されない)。

英語判例の処理
~~~~~~~~~~~~~~
`こちら <https://github.com/drowse314-dev-ymat/hanrei_getter>`_ で出力した英語の判例に関しては、日付のフォーマットの処理に
異なる対応が必要なため、以下のように ``--english`` オプションを付与します。

.. code-block:: sh

    $ sh ex_abst.sh english_hanrei_collection target_dir --english
