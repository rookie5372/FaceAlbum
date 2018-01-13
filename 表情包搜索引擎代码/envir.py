#!/usr/bin/env python
# -*- coding=utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import sys
import os
import lucene


from java.io import File
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.index import DirectoryReader
from org.apache.lucene.queryparser.classic import QueryParser
from org.apache.lucene.store import SimpleFSDirectory
from org.apache.lucene.search import IndexSearcher
from org.apache.lucene.util import Version
from org.apache.lucene.analysis.core import WhitespaceAnalyzer
from org.apache.lucene.analysis.miscellaneous import LimitTokenCountAnalyzer

from org.apache.lucene.index import DirectoryReader
from org.apache.lucene.queryparser.classic import QueryParser
from org.apache.lucene.store import SimpleFSDirectory
from org.apache.lucene.search import IndexSearcher
from org.apache.lucene.util import Version
from org.apache.lucene.search import BooleanQuery
from org.apache.lucene.search import BooleanClause
from org.apache.lucene.search.spell import SpellChecker
from org.apache.lucene.search.spell import LuceneDictionary
from org.apache.lucene.index import IndexReader
from org.apache.lucene.index import IndexWriterConfig

vm_env = lucene.initVM(vmargs=['-Djava.awt.headless=true'])
directory = SimpleFSDirectory(File("store"))
searcher = IndexSearcher(DirectoryReader.open(directory))
# 创建拼写检查索引
spell_dic = SimpleFSDirectory(File("spellchecker"))
spellchecker = SpellChecker(spell_dic)
analyzer = StandardAnalyzer(Version.LUCENE_CURRENT)
