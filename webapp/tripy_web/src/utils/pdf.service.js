import jsPDF from 'jspdf';

const PDFGenerator = {
    getTripsPdf(trips){
        var doc = new jsPDF()
        var line = 1
        doc.text("Here are your trips for the next 30 days!", 10, 10*line++)
        trips.forEach(trip => {
            doc.text(trip.destination + "( starting " + trip.start_date + " )" , 10, 10*line++)
        });
        doc.save('my-trips.pdf')
    }
}

export { PDFGenerator }
