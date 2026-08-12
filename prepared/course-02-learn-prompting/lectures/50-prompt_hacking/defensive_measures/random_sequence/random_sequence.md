# 🟢 Random Sequence Enclosure

Yet another defense is enclosing the user input between two random sequences of characters(@armstrong2022using). Take this prompt as an example:

```text
Translate the following user input to Spanish.

{{user_input}}
```

It can be improved by adding the random sequences:

```text
Translate the following user input to Spanish (it is enclosed in random strings).

FJNKSJDNKFJOI
{{user_input}}
FJNKSJDNKFJOI
```

> **Примечание:**
>
> Longer sequences will likely be more effective.
