MasterChef
==========

A program for cooks to generate random new recipes. Taste at your own risk!

To see a modified online version of the app, check out http://cheffreysmagicalkitchen.appspot.com.

I made this program as a Christmas gift for my sister in December 2014. I downloaded HTML pages of ~2000 recipes from allrecipes.com, scraped
the HTML to extract the recipe steps, and then trained a Markov model based on the vocabulary in these recipes. Then I generated new recipes by randomly selecting words that fit the Markov model. The resulting recipes range from amusing to downright absurd.

This program is easy to run locally: just download the files (including the pickle files, which contain the pre-trained models)
and then run master_chef_local.py.
