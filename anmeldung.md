---
layout: page
title: "Anmeldung für das nächste Dojo"
permalink: /anmeldung/
---

<form onsubmit="window.location = 'mailto:klub-coderdojo-sprecher@hpi.de?subject=[Anmeldung CoderDojo]&body=Hallo,%0Ahiermit möchte ich ' + name.value + ' für das nächste CoderDojo anmelden. Er/Sie ist ' + age.value + ' Jahre alt.'; return false; + '/' ">
    <input type="text" name="name" placeholder="Name">
    <input type="number" name="age" placeholder="Alter">
    <p>Vergiss bitte nicht die ausgefüllten und unterschriebenen <a href="/assets/Teilnahmebedingungen-CoderDojo-Potsdam.pdf">Teilnahmebedingungen</a>!</p>
    <input type="submit" value="Dabei sein!" class="btn">
</form>
