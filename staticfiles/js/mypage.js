

document.addEventListener('DOMContentLoaded', function() {
    // infoUpdateクリック時の処理
    const infoUpdateButton = document.getElementById('infoUpdate');
    const logoutButton = document.getElementById('logout-button');
    const scheduleButton = document.getElementById('schedule-button');
    const reviewButton = document.getElementById('review-button');
    const favoriteButton = document.getElementById('favorite-button');
    const withdrawalButton = document.getElementById('withdrawal-button');
    const rankButton = document.getElementById('rank-button');

    if (infoUpdateButton) {
        infoUpdateButton.addEventListener('click', function() {
            const userInfoDiv = document.getElementById('user-info');
            if (userInfoDiv) {
                const memberInfo = `
                    <h2>会員情報</h2>
                    <p>名前: ${userInfoDiv.dataset.firstName} ${userInfoDiv.dataset.lastName}</p>
                    <p>メール: ${userInfoDiv.dataset.email}</p>
                    <p>会員ID: ${userInfoDiv.dataset.accountId}</p>
                    <p>会員ランク: ${userInfoDiv.dataset.rank}</p>
                    <p><a href="${userInfoDiv.dataset.url1}">会員情報を変更する</a></p>
                    <p><a href="${userInfoDiv.dataset.url2}">パスワードを変更する</a></p>
                    `;
                // mContentに表示する
                document.querySelector('.mContent').innerHTML = memberInfo;
            }
        });
    }

    // logoutクリック時の処理
    if (logoutButton) {
        logoutButton.addEventListener('click', function() {
            const logoutInfoDiv = document.getElementById('logout-info');
            if (logoutInfoDiv) {
                const logout = `
                    <h2>ログアウトしますか？</h2>
                    <br>
                    <p><a href="${logoutInfoDiv.dataset.yes}">はい</a></p>
                `;
                // mContentに表示する
                document.querySelector('.mContent').innerHTML = logout;
            }
        });
    }

    if (scheduleButton) {
        scheduleButton.addEventListener('click', function() {
            const scheduleInfoDiv = document.getElementById('schedule-info');
            if (scheduleInfoDiv) {
                try {
                    const dataJsonSchedule = scheduleInfoDiv.dataset.schedule;
                    const scheduleData = dataJsonSchedule ? JSON.parse(dataJsonSchedule) : null;

                    // scheduleDataがnullまたは空配列かをチェック
                    if (!scheduleData || scheduleData.length === 0) {
                        document.querySelector('.mContent').innerHTML = `<p>予約がありません</p>`;
                        return;  // 処理を終了
                    }

                    let schedule = `
                        <h2>あなたの予約履歴</h2>
                        <table>
                            <tr>
                                <th>店名</th>
                                <th>開始日程</th>
                                <th>開始時刻</th>
                                <th>予約者</th>
                                <th>予約人数</th>
                                <th>予約キャンセル</th>
                            </tr>
                    `;
                    scheduleData.forEach(item => {
                        schedule += `
                            <tr>
                                <td>${item.shop_name}</td>
                                <td>${item.startDate}</td>
                                <td>${item.startHour}</td>
                                <td>${item.name}</td>
                                <td>${item.numbers}</td>
                                <td><a href="${item.cancel_url}">キャンセル</a></td>
                            </tr>
                        `;
                    });
                    schedule +=  `</table>`      
                    document.querySelector('.mContent').innerHTML = schedule;
                } catch(error) {
                    console.log(error)
                }
            }    
        });
    }

    if (reviewButton) {
        reviewButton.addEventListener('click', function() {
            const reviewInfoDiv = document.getElementById('review-info');
            if (reviewInfoDiv) {
                try {
                    const dataJsonReview = reviewInfoDiv.dataset.review;
                    const reviewData = dataJsonReview ? JSON.parse(dataJsonReview) : null;

                    // reviewDataがnullまたは空配列かをチェック
                    if (!reviewData || reviewData.length === 0) {
                        document.querySelector('.mContent').innerHTML = `<p>レビューがありません</p>`;
                        return;  // 処理を終了
                    }
                    
                    let review = `
                        <h2>あなたのレビュー履歴</h2>
                        <table>
                            <thead>
                                <tr>
                                    <th>店名</th>
                                    <th>レビュー星</th>
                                    <th>コメント</th>
                                    <th>編集</th>
                                </tr>
                            </thead>
                    `;
                    reviewData.forEach(item => {
                        review += `
                            <tr>
                                <td>${item.reviewShopName}</td>
                                <td>${'★'.repeat(item.reviewStar)}</td>
                                <td>${item.reviewComment}</td>
                                <td><a href="${item.cancel_url_review}">編集</a></td>
                            </tr>
                        `;
                    });
                    review +=  `</table>`      
                    document.querySelector('.mContent').innerHTML = review;
                } catch(error) {
                    console.log(error)
                }
            }    
        });
    }

    if (favoriteButton) {
        favoriteButton.addEventListener('click', function() {
            const favoriteInfoDiv = document.getElementById('favorite-info');
            const favoriteData = favoriteInfoDiv.dataset.favorite;
    
            // JSONデータのパースとエラーチェック
            let dataJsonFavorite;
            try {
                dataJsonFavorite = JSON.parse(favoriteData);
            } catch (e) {
                console.error("JSONのパースに失敗しました:", e);
                document.querySelector('.mContent').innerHTML = "<p>データの読み込みに失敗しました。</p>";
                return;
            }
    
            // パース結果が配列でデータが存在するかのチェック
            if (Array.isArray(dataJsonFavorite) && dataJsonFavorite.length > 0) {
                const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');

                let favoriteContent = `
                    <h2>あなたのお気に入り店舗</h2>
                    <form action="" method="POST">
                    <input type="hidden" name="csrfmiddlewaretoken" value="${csrfToken}">
                `;
                dataJsonFavorite.forEach(item => {
                    favoriteContent += `
                        <label><input type="radio" class="delete-shop" name="delete-shop" value="${item.shopName}">${item.shopName}</label>
                        <br>
                    `;
                });
                favoriteContent += `
                    <br>
                    <button type="submit" name="delete-favorite-shop">選択したお気に入り店舗を削除</button>
                    </form>
                `;
                document.querySelector('.mContent').innerHTML = favoriteContent;
            } else {
                document.querySelector('.mContent').innerHTML = "<p>お気に入り店舗がありません。</p>";
            }
        });
    }
    if (withdrawalButton) {
        withdrawalButton.addEventListener('click', function() {
            const withdrawalInfoDiv = document.getElementById('withdrawal-info');
            const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');

            if (withdrawalInfoDiv) {
                const withdrawal = `
                    <h2>本当に本アプリから退会しますか？</h2>
                    <p>※削除されたアカウントは復元出来ません。</p>
                    <br>
                    <form action="" method="POST">
                    <input type="hidden" name="csrfmiddlewaretoken" value="${csrfToken}">
                    <button type="submit" name="withdrawal-membership">退会する</button>
                    </form>
                `;
                // mContentに表示する
                document.querySelector('.mContent').innerHTML = withdrawal;
            }
        });
    }
    if (rankButton) {
        rankButton.addEventListener('click', function() {
            const rankInfoDiv = document.getElementById('rank-info');
            const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
            const rankData = rankInfoDiv.dataset.rank;
            if (rankInfoDiv) {
                const rank = `
                    <h2>有料会員に登録</h2>
                    <p>月額300円のサブスクリプションプランです。</p>
                    <br>
                    <a href="${rankData}">有料会員登録手続きへ進む</a>
                `;
                // mContentに表示する
                document.querySelector('.mContent').innerHTML = rank;
            }
        });
    }
});