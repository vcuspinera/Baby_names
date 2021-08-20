# Load libraries

# General libraries

import pandas as pd
import numpy as np
import time
import re
from nltk.tokenize import word_tokenize

# To get IPA (International Phonetic Alphabet)

import eng_to_ipa as ipa
import epitran
epi = epitran.Epitran('spa-Latn')


# Class
class Names_rhyme:
    """
    A class that look for rhymes in given names.
    """
    
    def __init__(self):
        self.name1 = ""
        self.name2 = ""
        self.complete_name = ""

    def check_two_names(self, name1, name2):
        """
        Function that compares two given names using International Phonetic
        Alphabet (IPA) in English and Spanish to compare vowels and syllables
        to check of Rhymes and Phonaesthetics, and returns scores for the
        Spanish, English and Total comparison.
        
        Parameters
        -------------
        name1 : (str)
            one word that represents one first name or surname.
        name2 : (name1)
            one word that represents one first name or surname.
            
        Returns
        -------------
        (list) list of scores for the Spanish, English and Total comparison.
        
        Example
        -------------
        v = Names_rhyme()
        v.check_two_names("elisa", "cuspinera")
        (output:) (0.1667, 0.6667, 0.4167)
        """
        # Get last word of each line without punctuation
        punctuation = '!"#$%&()*+,-./:;<=>?@[\\]^_`{|}~'
        self.name1 = name1
        self.name2 = name2

        # Convert names to IPA
        # ...in english
        self.ipa_e1 = "kʊzpɪˈnirə" if self.name1 == 'cuspinera' else ipa.convert(self.name1)
        self.ipa_e2 = "kʊzpɪˈnirə" if self.name2 == 'cuspinera' else ipa.convert(self.name2)
        # ...in spanish
        self.ipa_s1 = epi.transliterate(self.name1)
        self.ipa_s2 = epi.transliterate(self.name2)

        # Get last vowel in IPA
        # convert diphiongs in other codes
        for diphthong in [('aʊ', '1'), ('aɪ', '2'), ('ər', '3'), ('oʊ', '4'),
                          ('ɔɪ', '5'), ('eɪ', '6')]:
            self.ipa_e1 = self.ipa_e1.replace(diphthong[0], diphthong[1])
            self.ipa_e2 = self.ipa_e2.replace(diphthong[0], diphthong[1])
        # vowels
        vowels = 'ɑæʌɔəɚɛɝɪɨiʊuʉaeo123456'
        
        try:
            # ...in english
            #    ...last 1 vowel in english
            vowel_e1_1 = "".join([c for c in self.ipa_e1 if c in vowels])[-1]
            vowel_e1_2 = "".join([c for c in self.ipa_e2 if c in vowels])[-1]
            #    ...last 2 vowels in english
            vowel_e2_1 = "".join([c for c in self.ipa_e1 if c in vowels])[-2:]
            vowel_e2_2 = "".join([c for c in self.ipa_e2 if c in vowels])[-2:]
            #    ...last 3 letters in english
            syllable_e1 = self.ipa_e1[-3:]
            syllable_e2 = self.ipa_e2[-3:]
            #    ...initial 2 letters in english
            init_e1 = self.ipa_e1[:2]
            init_e2 = self.ipa_e1[:2]

            # ...in spanish
            #    ...last 1 vowel in spanish
            vowel_s1_1 = "".join([c for c in self.ipa_s1 if c in vowels])[-1:]
            vowel_s1_2 = "".join([c for c in self.ipa_s2 if c in vowels])[-1:]
            #    ...last 2 vowels in spanish
            vowel_s2_1 = "".join([c for c in self.ipa_s1 if c in vowels])[-2:]
            vowel_s2_2 = "".join([c for c in self.ipa_s2 if c in vowels])[-2:]
            #    ...last 3 letters in spanish
            syllable_s1 = self.ipa_s1[-3:]
            syllable_s2 = self.ipa_s2[-3:]
            #    ...initial 2 letters in spanish
            init_s1 = self.ipa_s1[:2]
            init_s2 = self.ipa_s2[:2]

            # Comparisons
            vow_e1 = vowel_e1_1==vowel_e1_2
            vow_e2 = vowel_e2_1==vowel_e2_2
            vow_s1 = vowel_s1_1==vowel_s1_2
            vow_s2 = vowel_s2_1==vowel_s2_2
            syllable_e = syllable_e1==syllable_e2
            syllable_s = syllable_s1==syllable_s2
            init_e = init_e1==init_e2
            init_s = init_s1==init_s2

            # get scores
            score = np.round(sum([vow_e1, 2*vow_e2, vow_s1, 2*vow_s2, 2*syllable_e, 2*syllable_s, init_e, init_s])/12, 4)
            score_sp = np.round(sum([vow_s1, 2*vow_s2, 2*syllable_s, init_s])/6, 4)
            score_en = np.round(sum([vow_e1, 2*vow_e2, 2*syllable_e, init_e])/6, 4)
            
        except:
            # this except is because there are some names as 'bg' that doesn't have any vowels
            score = 0; score_sp = 0; score_en = 0
        return (score_sp, score_en, score)

    def check_complete_name(self, complete_name):
        """
        Function that compares two given names using International Phonetic
        Alphabet (IPA) in English and Spanish to compare vowels and syllables
        to check of Rhymes and Phonaesthetics, and returns scores for the
        Spanish, English and Total comparison.
        
        Parameters
        -------------
        complete_name : (str)
            string with a complete name with first name(s) and family name(s).

        Returns
        -------------
        (list) list of scores for the Spanish, English and Total comparison.
        
        Example
        -------------
        v = Names_rhyme()
        score = v.check_complete_name("elisa macarena cuspinera martinez")
        (output:) (0.1667, 0.4167, 0.2917)
        """
        # variables
        self.complete_name = complete_name.lower()
        score=0; score_en=0; score_sp=0
        n = len(self.complete_name.split())
        k=1
        
        # split the 'complete_name' string
        if "cuspinera" in self.complete_name.split():
            the_name = ""
            for i in self.complete_name.split():
                the_name += "kʊzpɪˈnirə" if i=='cuspinera' else ipa.convert(i)
                if k != n:
                    the_name += " "; k += 1
            self.ipa_english = the_name
        else:
            self.ipa_english = ipa.convert(self.complete_name)
        self.ipa_spanish = epi.transliterate(self.complete_name)
        
        # get scores
        for i in np.arange(0, n):
            for j in np.arange(i+1, n):
                aux_sp, aux_en, aux_tot = self.check_two_names(self.complete_name.split()[i], self.complete_name.split()[j])
                score += aux_tot
                score_en += aux_en
                score_sp += aux_sp
        return (np.round(score_sp/(n*(n-1)/2), 4), np.round(score_en/(n*(n-1)/2), 4), np.round(score/(n*(n-1)/2), 4))