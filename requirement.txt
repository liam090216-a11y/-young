import streamlit as st
import streamlit.components.v1 as components

# 페이지 기본 설정
st.set_page_config(
    page_title="스트림릿 벽돌 깨기 게임",
    page_icon="🧱",
    layout="centered"
)

st.title("🧱 클래식 벽돌 깨기 (Breakout)")
st.caption("좌우 화살표 키(← / →) 또는 마우스/터치로 패들을 움직여 보세요!")

# HTML5 Canvas + JS 기반 벽돌 깨기 게임 코드
game_html = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8" />
    <style>
        * { padding: 0; margin: 0; box-sizing: border-box; }
        body { 
            background: #0f172a; 
            display: flex; 
            flex-direction: column;
            justify-content: center; 
            align-items: center; 
            min-height: 100vh;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            color: white;
        }
        canvas { 
            background: #1e293b; 
            display: block; 
            border-radius: 12px;
            box-shadow: 0 10px 25px rgba(0,0,0,0.5);
        }
        .btn {
            margin-top: 15px;
            padding: 10px 24px;
            font-size: 16px;
            font-weight: bold;
            color: white;
            background: #3b82f6;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            transition: 0.2s;
        }
        .btn:hover { background: #2563eb; }
    </style>
</head>
<body>

<canvas id="myCanvas" width="480" height="400"></canvas>
<button class="btn" onclick="document.location.reload()">🎮 다시 시작</button>

<script>
    const canvas = document.getElementById("myCanvas");
    const ctx = canvas.getContext("2d");

    // 공 설정
    let x = canvas.width / 2;
    let y = canvas.height - 30;
    let dx = 3;
    let dy = -3;
    const ballRadius = 8;

    // 패들 설정
    const paddleHeight = 12;
    const paddleWidth = 85;
    let paddleX = (canvas.width - paddleWidth) / 2;

    // 조작키 설정
    let rightPressed = false;
    let leftPressed = false;

    // 벽돌 설정
    const brickRowCount = 4;
    const brickColumnCount = 6;
    const brickWidth = 65;
    const brickHeight = 18;
    const brickPadding = 10;
    const brickOffsetTop = 40;
    const brickOffsetLeft = 20;

    // 점수 및 생명
    let score = 0;
    let lives = 3;

    // 벽돌 배열 초기화
    const bricks = [];
    for (let c = 0; c < brickColumnCount; c++) {
        bricks[c] = [];
        for (let r = 0; r < brickRowCount; r++) {
            bricks[c][r] = { x: 0, y: 0, status: 1 };
        }
    }

    // 이벤트 리스너 (키보드 & 마우스)
    document.addEventListener("keydown", keyDownHandler, false);
    document.addEventListener("keyup", keyUpHandler, false);
    document.addEventListener("mousemove", mouseMoveHandler, false);

    function keyDownHandler(e) {
        if (e.key === "Right" || e.key === "ArrowRight") rightPressed = true;
        else if (e.key === "Left" || e.key === "ArrowLeft") leftPressed = true;
    }

    function keyUpHandler(e) {
        if (e.key === "Right" || e.key === "ArrowRight") rightPressed = false;
        else if (e.key === "Left" || e.key === "ArrowLeft") leftPressed = false;
    }

    function mouseMoveHandler(e) {
        const relativeX = e.clientX - canvas.offsetLeft;
        if (relativeX > 0 && relativeX < canvas.width) {
            paddleX = relativeX - paddleWidth / 2;
        }
    }

    // 충돌 감지
    function collisionDetection() {
        for (let c = 0; c < brickColumnCount; c++) {
            for (let r = 0; r < brickRowCount; r++) {
                const b = bricks[c][r];
                if (b.status === 1) {
                    if (x > b.x && x < b.x + brickWidth && y > b.y && y < b.y + brickHeight) {
                        dy = -dy;
                        b.status = 0;
                        score += 10;
                        if (score === brickRowCount * brickColumnCount * 10) {
                            alert("🎉 축하합니다! 모든 벽돌을 깨트렸습니다!");
                            document.location.reload();
                        }
                    }
                }
            }
        }
    }

    // 공 그리기
    function drawBall() {
        ctx.beginPath();
        ctx.arc(x, y, ballRadius, 0, Math.PI * 2);
        ctx.fillStyle = "#f43f5e";
        ctx.fill();
        ctx.closePath();
    }

    // 패들 그리기
    function drawPaddle() {
        ctx.beginPath();
        ctx.rect(paddleX, canvas.height - paddleHeight - 10, paddleWidth, paddleHeight);
        ctx.fillStyle = "#38bdf8";
        ctx.fill();
        ctx.closePath();
    }

    // 벽돌 그리기
    function drawBricks() {
        const colors = ["#f59e0b", "#10b981", "#6366f1", "#ec4899"];
        for (let c = 0; c < brickColumnCount; c++) {
            for (let r = 0; r < brickRowCount; r++) {
                if (bricks[c][r].status === 1) {
                    const brickX = c * (brickWidth + brickPadding) + brickOffsetLeft;
                    const brickY = r * (brickHeight + brickPadding) + brickOffsetTop;
                    bricks[c][r].x = brickX;
                    bricks[c][r].y = brickY;
                    ctx.beginPath();
                    ctx.rect(brickX, brickY, brickWidth, brickHeight);
                    ctx.fillStyle = colors[r % colors.length];
                    ctx.fill();
                    ctx.closePath();
                }
            }
        }
    }

    // 점수 및 목숨 표시
    function drawScore() {
        ctx.font = "bold 14px sans-serif";
        ctx.fillStyle = "#94a3b8";
        ctx.fillText("SCORE: " + score, 20, 25);
    }

    function drawLives() {
        ctx.font = "bold 14px sans-serif";
        ctx.fillStyle = "#94a3b8";
        ctx.fillText("LIVES: " + lives, canvas.width - 80, 25);
    }

    // 메인 루프
    function draw() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        drawBricks();
        drawBall();
        drawPaddle();
        drawScore();
        drawLives();
        collisionDetection();

        // 좌우 벽 충돌
        if (x + dx > canvas.width - ballRadius || x + dx < ballRadius) {
            dx = -dx;
        }
        
        // 천장 충돌
        if (y + dy < ballRadius) {
            dy = -dy;
        } else if (y + dy > canvas.height - ballRadius - 10) {
            // 패들 충돌 조건
            if (x > paddleX && x < paddleX + paddleWidth) {
                dy = -dy;
            } else if (y + dy > canvas.height - ballRadius) {
                // 바닥 충돌 (생명 차감)
                lives--;
                if (!lives) {
                    alert("GAME OVER 😢");
                    document.location.reload();
                } else {
                    x = canvas.width / 2;
                    y = canvas.height - 30;
                    dx = 3;
                    dy = -3;
                    paddleX = (canvas.width - paddleWidth) / 2;
                }
            }
        }

        // 패들 이동 처리
        if (rightPressed && paddleX < canvas.width - paddleWidth) {
            paddleX += 6;
        } else if (leftPressed && paddleX > 0) {
            paddleX -= 6;
        }

        x += dx;
        y += dy;
        requestAnimationFrame(draw);
    }

    draw();
</script>

</body>
</html>
"""

# Streamlit에 HTML 코드 렌더링 (높이 및 너비 지정)
components.html(game_html, height=500)
