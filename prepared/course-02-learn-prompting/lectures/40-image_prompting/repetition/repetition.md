# 🟢 Repetition

Repeating the same word within a prompt, or similar phrases can cause the model
to emphasize that word in the generated image(@oppenlaender2022taxonomy). For example, [@Phillip Isola](https://twitter.com/phillip_isola/status/1532189632217112577) generated these waterfalls with DALLE:

`A beautiful painting of a mountain next to a waterfall.`.

  <!-- изображение (не скопировано) -->

`A very very very very very very very very very very very very very very very very very very very very very very beautiful painting of a mountain next to a waterfall.`

  <!-- изображение (не скопировано) -->

The emphasis on the word `very` seems to improve generation quality! Repetition can
also be used to emphasize subject terms. For example, if you want to generate an image
of a planet with aliens, using the prompt `A planet with aliens aliens aliens aliens aliens aliens aliens aliens aliens aliens aliens aliens`
will make it more likely that aliens are in the resultant image. The following images are made with Stable Diffusion.

`A planet with aliens`

  <!-- изображение (не скопировано) -->

`A planet with aliens aliens aliens aliens aliens aliens aliens aliens aliens aliens aliens aliens`

  <!-- изображение (не скопировано) -->

## Notes

This method is not perfect, and using weights (next article) is often a better option.
