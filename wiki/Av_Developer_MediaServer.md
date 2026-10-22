---
title: "Av:Developer:MediaServer"
permalink: "/wiki/Av:Developer:MediaServer"
redirect_from:
---

{% raw %}
Here is the proposed request syntax:

    Request             ::= "in" (Category) (Filter)* "report" ("value" Tag With* | "items" Give+ Sort*)\n
    Category            ::= "audio" | "video" | "photo" | "text"
    Filter              ::= Where | Search
    Where               ::= "where" Tag "=" Value
    Search              ::= "search" Value
    Give                ::= "give" Tag With*
    With                ::= "with" Tag
    Sort                ::= "sort" Tag
    Tag                 ::= Text-Without-Spaces
    Value               ::= (Word | String)
    Word                ::= Text-Without-Spaces
    String              ::= '"' Text-Without-Double-Quotes '"' | "'" Text-Without-Quotes "'"
{% endraw %}
