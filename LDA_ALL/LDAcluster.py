import gensim.corpora as corpora
import pandas as pd
import pyLDAvis.gensim_models
import regex as re
from gensim import models
from gensim.models import CoherenceModel
from gensim.models import LdaModel
from matplotlib import pyplot as plt
from nltk.corpus import stopwords

stop_words = stopwords.words('english')
# decide the number of models you want to get
NUM_ROUND = 16


def clean_text(text):
    # Remove URLs, mentions, and hashtags from the text
    # make all characters be lowercase
    text = text.lower()
    text = re.sub(r"[^a-zA-Z0-9]", " ", text)
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r'http\S+', '', text)
    text = re.sub(r'@\S+', '', text)
    text = re.sub(r'#\S+', '', text)
    text = re.sub(r"\d", "", text)
    # remove the emoji
    text = re.sub(r"\p{Emoji}", "", text)
    # meaningless length
    if len(text) <= 2:
        text = ""
    return text


# main function
# generate the dic and corpus for training
def LDA_implementation():
    df = pd.read_excel("../AR/abstract.xlsx")
    df.dropna(inplace=True)
    # first step cleaning
    df['Abstract'] = df['Abstract'].apply(lambda x: clean_text(x))
    df.dropna(inplace=True)
    abstracts = df['Abstract']
    # get the comments list
    abstract_list = abstracts.values
    # remove the stop words
    text_lists = [[word for word in d.lower().split() if word not in stop_words] for d in abstract_list]
    # build the dictionary
    dictionary = corpora.Dictionary(text_lists)
    # remove the most frequent words
    # After cleaning the word list, we use the gensim library to build a dictionary,
    # and use "filter_extremes()" to remove the words
    # that only appear in a very small or large portion of the document
    dictionary.filter_extremes()
    dictionary.filter_n_most_frequent(15)
    print(dictionary.most_common(20))
    # trun the text lists into word bag lists
    #  Finally,we use the dictionary and doc2bow functions in the gensim library to convert the text list
    #  into a bag-of-words corpus.
    corpus = [dictionary.doc2bow(text) for text in text_lists]

    #
    #
    # We can see that it is best when the topic is equal to 3.
    # The following is the analysis graph generated with pyLDAvis
    # view(num=3, corpus=corpus, dictionary=dictionary, version='r/ChatGPT')
    #
    """this code below is used to apply a pre-trained LDA_ALL model to a corpus, extract the major topic for each 
    document in the corpus, and add the major topic information to a pandas DataFrame. """
    # # Obtaining the main topic for each review:
    num = 5
    view(num, corpus, dictionary)
    # all_topics = optimal_model.get_document_topics(corpus)
    # all_topics_csr = gensim.matutils.corpus2csc(all_topics)
    # all_topics_numpy = all_topics_csr.T.toarray()
    # major_topic = [np.argmax(arr) for arr in all_topics_numpy]
    # df['major_topic'] = major_topic
    # depict(df, 'dataisbeautiful')


def train_model(corpus, dic):
    for i in range(1, NUM_ROUND):
        print('\n')
        print('nums of topic:{}'.format(i))
        temp = 'lda_{}'.format(i)
        tmp = LdaModel(corpus=corpus, num_topics=i, id2word=dic, passes=20)
        file_path = 'model/{}.model'.format(temp)
        tmp.save(file_path)
        print('------------------')


def plot_perplexity(corpus):
    x_list = []
    y_list = []
    for i in range(1, NUM_ROUND):
        temp_model = 'model/lda_{}.model'.format(i)
        try:
            lda = models.ldamodel.LdaModel.load(temp_model)
            perplexity = lda.log_perplexity(corpus)  # compute perplexity the lower the better
            x_list.append(i)
            y_list.append(perplexity)
        except Exception as e:
            print(e)
    plt.plot(x_list, y_list)
    plt.xlabel('num topics')
    plt.ylabel('perplexity score')
    plt.legend('perplexity_values', loc='best')
    plt.savefig('perplexity_values.png')
    plt.show()


def compute_coherence(corpus, dictionary):
    x_list = []
    y_list = []
    for i in range(1, NUM_ROUND):
        temp_model = 'model/lda_{}.model'.format(i)
        try:
            # load the model
            lda = models.ldamodel.LdaModel.load(temp_model)
            # compute the model's coherence score, the higher the better
            cv_tmp = CoherenceModel(model=lda, corpus=corpus, dictionary=dictionary, coherence='u_mass')
            # compute the coherence
            x_list.append(i)
            y_list.append(cv_tmp.get_coherence())
        except Exception as e:
            print(e)
            print('not found this model:{}'.format(temp_model))
    plt.rcParams['axes.unicode_minus'] = False
    plt.plot(x_list, y_list)
    plt.xlabel('num topics')
    plt.ylabel('coherence score')
    plt.legend('coherence_values', loc='best')
    plt.savefig('coherence_values.png')
    plt.show()


def view(num, corpus, dictionary, version="general"):
    model_name = 'model/lda_{}.model'.format(num)
    pos_model = models.ldamodel.LdaModel.load(model_name)
    pyLDAvis.enable_notebook()
    vis = pyLDAvis.gensim_models.prepare(pos_model, corpus, dictionary)
    pyLDAvis.save_html(vis, '{}_lad_{}_.html'.format(version[2:], num))


def depict(df, name='general'):
    # Plotting Data frequency for topics
    df['major_topic'].value_counts().sort_values(ascending=False).plot(kind='bar')
    plt.xlabel("Comment Topics")
    plt.ylabel("Number of Comments")
    plt.title("Topic wise Data Frequency--{}".format(name))
    plt.savefig('{}_topics.png'.format(name))
    plt.show()


LDA_implementation()
