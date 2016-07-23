from flask import Flask, render_template, request
from wtforms import Form, TextField, validators
import statistics

# import twitter_stream from local dir
import twitter_stream as twt

app = Flask(__name__)

class HashtagForm(Form):
    hashtag = TextField(u'#',
                        [validators.DataRequired(),
                        validators.length(min=2)])

@app.route('/')
def index():
    form = HashtagForm(request.form)
    return render_template('hashtagform.html', form=form)

@app.route('/results', methods=['POST'])
def results():
    form = HashtagForm(request.form)
    if request.method == 'POST' and form.validate():
        hashtag = request.form['hashtag']
        if twt.fetchAndSaveSamples(hashtag):
            twitter_dict = twt.getSentimentOfText(open("twitter_out.txt"))
            score_list = list(twitter_dict.values())

            nr_tweets = len(score_list)
            score_min = min(score_list)
            score_med = statistics.median(score_list)
            score_avg = round(statistics.mean(score_list), 2)
            score_max = max(score_list)
            score_total = sum(score_list)
            if score_total > 0:
                sent_total = "POSITIVE"
            elif score_total < 0:
                sent_total = "NEGATIVE"
            else:
                sent_total = "NEUTRAL"

            return render_template('results.html',
                                    hashtag=hashtag,
                                    nr_tweets=nr_tweets,
                                    score_min=score_min,
                                    score_med=score_med,
                                    score_avg=score_avg,
                                    score_max=score_max,
                                    score_total=score_total,
                                    sent_total=sent_total,
                                    twitter_dict=twitter_dict)
        else:
            return render_template('hashtagform.html', form=form, error="No results found!")
    return render_template('hashtagform.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)
