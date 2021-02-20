/**
 * Download a thing using libcurl
 * 
 * axios seems to poop itself on hail satan metal cover sometimes
 * maybe it's too big? libcurl is kinda annoying to use, so basically:
 *  - use libcurl for big binary downloads
 *  - axios for JSONish stuff
 */

const {Curl, CurlFeature} = require("node-libcurl");
const path = require("path");

// 3 minute timeout
module.exports = (URL, timeout=180) => {


    return new Promise((resolve, reject) => {
        const curl = new Curl();

        curl.enable(CurlFeature.NoDataParsing);
        curl.setOpt(Curl.option.NOPROGRESS, 1);
        curl.setOpt(Curl.option.FOLLOWLOCATION, 1);
        curl.setOpt(Curl.option.TIMEOUT, timeout);
        curl.setOpt(Curl.option.CAINFO, path.join(process.cwd(), "conf/cert.pem"));

        curl.setOpt(Curl.option.URL, URL);

        curl.on('error', (err) => {
            curl.close.bind(curl);
            reject(err);
        });

        curl.on('end', (statusCode, data, headers) => {
            curl.close();
            resolve({statusCode, data, headers});
        });

        curl.perform();
    })
}