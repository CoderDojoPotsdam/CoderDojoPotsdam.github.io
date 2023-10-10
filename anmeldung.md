---
layout: page
title: "Anmeldung"
permalink: /anmelden/
---

<form onsubmit="window.location = 'mailto:klub-coderdojo-sprecher@hpi.de?subject=[Anmeldung CoderDojo]&body=Hallo,%0Ahiermit möchte ich ' + name.value + ' für das nächste CoderDojo anmelden. Er/Sie ist ' + age.value + ' Jahre alt.'; return false; + '/' ">
    <label for="name">Name</label>
    <input type="text" name="name"> <br>
    <label for="age">Alter</label>
    <input type="number" name="age"> <br>
    <input type="submit" value="Anmelden">
</form>
