//Eine Funktion, die aufgerufen wird, um ein Event zu löschen
function deleteEvent(eventId) { 
    // Ein 'fetch'-Aufruf, der eine Anfrage an den Server sendet
    fetch('/delete-event',{
        method: 'POST', // Die HTTP-Methode, hier POST, um Daten an den Server zu senden
        body: JSON.stringify({ eventId: eventId}) // Der Körper der Anfrage, hier die Event-ID im JSON-Format
    }). then((_res) => { // Nachdem die Anfrage verarbeitet wurde, wird diese Funktion ausgeführt
        window.location.href = "/"; // Leitet den Benutzer zur Hauptseite um
    });
}