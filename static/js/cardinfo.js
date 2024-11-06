document.addEventListener('DOMContentLoaded', function() {
    const stripe_APIKey = document.getElementById('stripe_APIKey').value;
    const user_pk = document.getElementById('user-pk').value;

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
                document.getElementById('error-message').textContent = result.error.message;
            } else {
                // DjangoのAPIエンドポイントにトークンを送信
                fetch('/credit/update-card/', {  // エンドポイントに合わせて変更
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ 
                        token: result.token.id,
                        kokyaku_pk: user_pk,
                    })
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        console.log("カード情報が更新されました。");
                    } else {
                        console.log("カード情報の更新に失敗しました。");
                    }
                });
            }
        });
    });
});