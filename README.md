# fire-detection-drone
Desenvolvimento de um drone de operação remota para a deteção e localização de focos de incêndio.

Explicação de código de visão e tratamento de imagem:
Numa primeira fase definimos a mascara para a cor que queremos rastrear através de umas trackbars. Posteriormente é calculado o dense optical flow para se poder obter a norma e angulo em radianos do vetor deslocamento. Para isto teve-se de fazer uma recolha dos vetores que estavam em movimento, obter a media destes e apresentar o valor caso fosse significativo. Assim poderemos ter uma noção de se o drone se está a deslocar por efeito do vento, por exemplo, e quanto se desloca.
