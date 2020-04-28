import { DateObj } from './DateObj';


export class CalendarTool {
    static calMonthCalendar(year, month) {
        let calendar = [[]];
        let firstDayOfMonth = new Date(year, month, 1);
        let lastDayOfMonth = new Date(year, month + 1, 0);
        let iterDay = new Date(year, month, 1 - firstDayOfMonth.getDay());
        while (!(iterDay.getDay() === 0 && iterDay > lastDayOfMonth)) {
            if (calendar[calendar.length - 1].length === 7) calendar.push([]);
            calendar[calendar.length - 1].push(new DateObj(iterDay));
            iterDay.setDate(iterDay.getDate() + 1);
        }
        return calendar;
    }

    static calYearCalendar(year) {
        let yearCalendar = {};
        for (let month = 0; month < 12; month++) {
            console.log('year', year, 'month', month);
            yearCalendar[month] = this.calMonthCalendar(year, month);
        }
        return yearCalendar;
    }

    static calThreeYearCalendar(year) {
        let threeYearCalander = {};
        threeYearCalander[year - 1] = this.calYearCalendar(year - 1);
        threeYearCalander[year] = this.calYearCalendar(year);
        threeYearCalander[year + 1] = this.calYearCalendar(year + 1);
        return threeYearCalander;
    }
}