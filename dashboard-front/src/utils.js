export default {
    humanFileSize(bytes) {
        let thresh = 1000;
        if(Math.abs(bytes) < thresh) {
            return bytes + ' B';
        }
        let units = ['kB','MB','GB','TB','PB','EB','ZB','YB'];
        let u = -1;
        do {
            bytes /= thresh;
            ++u;
        } while(Math.abs(bytes) >= thresh && u < units.length - 1);
        return bytes.toFixed(1)+' '+units[u];
    },
    zip (...rows) {
        return [...rows[0]].map((_,c) => rows.map(row => row[c]))
    }
}
