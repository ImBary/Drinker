Modele
======

.. automodule:: your_app.models
   :members:
   :undoc-members:
   :show-inheritance:

Drink
-----

Model reprezentujący napój w aplikacji.

.. py:class:: Drink

   .. py:attribute:: name
      :type: CharField

      Nazwa napoju.

   .. py:attribute:: description
      :type: TextField

      Opis napoju.

   .. py:attribute:: photo
      :type: ImageField

      Zdjęcie napoju.

   .. py:attribute:: ingrediens
      :type: TextField

      Lista składników napoju oddzielonych przecinkami.

   .. py:attribute:: instructon
      :type: TextField

      Instrukcja przygotowania napoju.

   .. py:attribute:: likes
      :type: IntegerField

      Liczba polubień napoju.

   .. py:attribute:: dislikes
      :type: IntegerField

      Liczba negatywnych ocen napoju.

   .. py:attribute:: taste_type
      :type: CharField

      Typ smaku napoju. Możliwe opcje: 'sweet', 'bitter', 'sour', 'salty', 'umami'.

   .. py:attribute:: strength
      :type: CharField

      Moc napoju. Możliwe opcje: 'non-alcoholic', 'light', 'medium', 'strong'.

   .. py:attribute:: temperature
      :type: CharField

      Preferowana temperatura podania. Możliwe opcje: 'hot', 'cold', 'warm'.

   .. py:attribute:: complexity
      :type: CharField

      Poziom złożoności przygotowania. Możliwe opcje: 'simple', 'moderate', 'complex'.

   .. py:attribute:: short_url
      :type: CharField

      Skrócony URL do strony napoju.

   .. py:attribute:: user
      :type: ForeignKey

      Użytkownik, który dodał napój.

UserVote
--------

Model reprezentujący głos użytkownika na napój.

.. py:class:: UserVote

   .. py:attribute:: user
      :type: ForeignKey

      Użytkownik, który oddał głos.

   .. py:attribute:: drink
      :type: ForeignKey

      Napój, na który oddano głos.

   .. py:attribute:: vote_type
      :type: CharField

      Typ głosu: 'like' lub 'dislike'.