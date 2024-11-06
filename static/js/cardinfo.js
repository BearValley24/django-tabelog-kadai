document.addEventListener('DOMContentLoaded', function() {
    var stripe_APIKey = document.getElementById('stripe_APIKey').value;
    console.log(stripe_APIKey);

    var stripe = Stripe(stripe_APIKey);
    var elements = stripe.elements();
    var card = elements.create('card');
    card.mount('#card-element-zone'); /* カード情報 */

    console.log(stripe)

    // フォームの送信時にトークン化
    var form = document.getElementById('payment-form');
    form.addEventListener('submit', function(event) {
    event.preventDefault();
    stripe.createToken(card).then(function(result) {
        if (result.error) {
        // エラー処理
        document.getElementById('error-message').textContent = result.error.message;
        } else {
        // トークンをサーバーに送信
        var token = result.token.id;
        // サーバーにトークンを送信して決済処理
        console.log(token);
        }
    });
    });
});