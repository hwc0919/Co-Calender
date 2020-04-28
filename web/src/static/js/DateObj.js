export class DateObj {

    constructor(date) {
        this.year = date.getFullYear();
        this.month = date.getMonth();
        this.day = date.getDate();
        this.dayOfWeek = date.getDay();
        this.ID = `${this.year}-${this.month}-${this.day}`;
        this.date = new Date(this.year, this.month, this.day);
    }

    toLocaleDateString() {
        return `${this.year}/${this.month + 1}/${this.day}`;
    }

    equals(dateObj) {
        return this.toLocaleDateString() === dateObj.toLocaleDateString();
    }

    isToday(dateObj) {
        return new Date().toLocaleDateString() === this.toLocaleDateString();
    }
}