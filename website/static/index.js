//Javascript backend code to delete the Event

function deleteEvent(eventId) {
    fetch('/delete-event',{
        method: 'POST',
        body: JSON.stringify({ eventId: eventId})
    }). then((_res) => {
        window.location.href = "/"; //redirect
    });
}