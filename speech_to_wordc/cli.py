import boto3
import json
import csv
from argparse import ArgumentParser
from janome.tokenizer import Tokenizer
from wordcloud import WordCloud
from collections import Counter, defaultdict

def counter(texts, parts):
    t = Tokenizer('neologd')
    words_count = defaultdict(int)
    words = []
    for text in texts:
        tokens = t.tokenize(text)
        for token in tokens:
            if token.part_of_speech.split(',')[0] in parts:
                if token.base_form not in ["こと", "よう", "そう", "これ", "それ", "さん", "ソレ", 'たい', 'みたい', 'かも']:
                    words_count[token.base_form] += 1
                    words.append(token.base_form)
    return words_count, words


def wordcloud(texts, parts, outputpath, fpath):
    words_count, words = counter(texts, parts)
    text = ' '.join(words)

    wordcloud = WordCloud(background_color="white",
        font_path=fpath, width=900, height=500).generate(text)

    wordcloud.to_file(outputpath)


def main() -> None:
    parser = ArgumentParser()
    parser.add_argument(
        '--bucket',
        help='S3 bucket name',
        required=True)
    parser.add_argument(
        '--file',
        help='S3 file name',
        required=True)
    parser.add_argument(
       '--output',
        help='output file path. default is out/wc_',
        default='speech_to_wordc/out/wc_')
    #parser.add_argument(
    #   '--notword',
    #    help='not word list',
    #    default='notword.txt')
    #parser.add_argument(
    #   '--dic',
    #    help='dic file')
    parser.add_argument(
       '--font',
        help='font filepath',
        default='speech_to_wordc/Meiryo.ttf')

    args = parser.parse_args()

    s3 = boto3.resource('s3')
    obj = s3.Object(args.bucket, args.file)

    body = obj.get()['Body'].read()

    data = json.loads(body.decode('utf-8'))
    texts = data['results']['transcripts'][0]['transcript'].split(' ')
    
    wordcloud(texts, ['名詞', '固有名詞'], args.output + 'noun.png', args.font)
    wordcloud(texts, ['副詞'], args.output + 'adv.png', args.font)
    wordcloud(texts, ['形容詞'], args.output + 'adj.png', args.font)
