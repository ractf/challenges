const crypto = require("crypto")

exports.hash = function(content) {
    // Super secret combination of hashing algos
    let hash = crypto.createHash('sha256').update(content).digest('base64')
    hash = crypto.createHash('md5').update(hash).digest('hex')
    return hash.toString().split("").reverse().join("")
}