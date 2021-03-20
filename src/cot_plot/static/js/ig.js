function connectToLightstreamer(itemList, fieldList){
// include the Lightstreamer Subscription module using require.js
    require(["Subscription"], function (Subscription) {

    var subscription = new Subscription(
        "MERGE",
        itemList, // e.g. {"MARKET:IX.D.FTSE.DAILY.IP","MARKET:MT.D.GC.MONTH1.IP"}
        fieldList // e.g. {"BID", "OFFER"}
    );

    // Set up Lightstreamer event listener
    subscription.addListener({
        onSubscription: function () {
            console.log('subscribed');
        },
        onUnsubscription: function () {
            console.log('unsubscribed');
        },
        onSubscriptionError: function (code, message) {
            console.log('subscription failure: ' + code + " message: " + message);
        },
        onItemUpdate: function (updateInfo) {
            // Lightstreamer published some data
            var epic = updateInfo.getItemName().split(":")[1];
            updateInfo.forEachField(function (fieldName, fieldPos, value) {
                    console.log('Field: ' + fieldName + " Value: " + value);
                    // Alternatively, if the field is JSON, such as in a confirm message:
                    var confirm = JSON.parse(value);
                    console.log('json: ' + confirm.dealId)
            }
        });
        }
    });

    // Subscribe to Lightstreamer
    lsClient.subscribe(subscription);
}
lsClient.unsubscribe(subscription);
lsClient.closeConnection();  
