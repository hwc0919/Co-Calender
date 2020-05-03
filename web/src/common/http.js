import Vue from 'vue';

// Restful API regulation: {success: Boolean, message: String, data: any}

export function request(options, method) {
    options.url = 'http://192.168.0.105:5000' + options.url.replace('/api', '');
    console.log(options);
    return new Promise((resolve, reject) => {
        uni.request({
            dataType: 'json', // default dataType
            method: method || 'GET', // default method
            ...options,
            success: ({ data, statusCode, header }) => {
                console.log('resp', data);
                console.log('statusCode', statusCode);
                console.log('header', header);
                if (statusCode !== 200) {
                    uni.showToast({
                        icon: 'none',
                        title: data.message || `操作失败, 状态码${statusCode}`,
                        duration: 1500
                    });
                    reject(data.message);
                }
                if (!data.success) {
                    uni.showToast({
                        icon: 'none',
                        title: data.message || `操作失败, 状态码${statusCode}`,
                        duration: 1500
                    });
                    reject(data.message || `操作失败, 状态码${statusCode}`);
                }
                resolve(data);
            },
            fail: (err) => {
                console.log('err', err);
                uni.showToast({
                    icon: 'none',
                    title: `操作失败`,
                    duration: 1500
                });
                reject('操作失败');
            }
        });
    });
}

export const http = {
    get: (options) => {
        return request(options, 'GET');
    },
    post: (options) => {
        return request(options, 'POST');
    }
};
