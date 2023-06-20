import random
import sys
import pygame as pg


WIDTH, HEIGHT = 1600, 900
delta = {
    pg.K_UP: (0, -5),
    pg.K_DOWN: (0, +5),
    pg.K_LEFT: (-5, 0),
    pg.K_RIGHT: (+5, 0),
}


def check_bound(rect: pg.Rect) -> tuple[bool, bool]:
    """
    こうかとんRect, 爆弾Rectが画面外 or 画面内かを判定する関数
    引数: こうかとんRect or 爆弾Rect
    戻り値: 横方向, 縦方向の判定結果タプル（True: 画面内, False: 画面外）
    """
    yoko, tate = True, True
    if rect.left < 0 or WIDTH < rect.right:  # 横方向判定
        yoko = False
    if rect.top < 0 or HEIGHT < rect.bottom:  # 縦方向判定
        tate = False
    return yoko, tate


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("ex02/fig/pg_bg.jpg")
    kk_img = pg.image.load("ex02/fig/3.png")  # こうかとんの画像
    kk_img = pg.transform.rotozoom(kk_img, 0, 2.0)
    kk_img_reverse = pg.image.load("ex02/fig/3.png")  # こうかとんの画像(反転)
    kk_img_reverse = pg.transform.flip(kk_img_reverse, False, True)
    kk_img_reverse = pg.transform.rotozoom(kk_img_reverse, 0, 2.0)
    kk_img_lst = {  # 8方向のこうかとんの辞書
        (0, -5): pg.transform.rotozoom(kk_img, -90, 1.0),
        (5, -5): pg.transform.rotozoom(kk_img_reverse, 225, 1.0),
        (5, 0): pg.transform.rotozoom(kk_img_reverse, 180, 1.0),
        (5, 5): pg.transform.rotozoom(kk_img_reverse, 135, 1.0),
        (0, 5): pg.transform.rotozoom(kk_img, 90, 1.0),
        (-5, 5): pg.transform.rotozoom(kk_img, 45, 1.0),
        (-5, 0): pg.transform.rotozoom(kk_img, 0, 1.0),
        (0, 0): pg.transform.rotozoom(kk_img, 0, 1.0),
        (-5, -5): pg.transform.rotozoom(kk_img, -45, 1.0),
    }
    # こうかとんSurface（kk_img）からこうかとんRect（kk_rct）を抽出する
    kk_rct = kk_img.get_rect()
    kk_rct.center = 900, 400
    bd_img = pg.Surface((20, 20))  # 練習１
    bd_img.set_colorkey((0, 0, 0))  # 黒い部分を透明にする
    pg.draw.circle(bd_img, (255, 0, 0), (10, 10), 10)
    x = random.randint(0, WIDTH)
    y = random.randint(0, HEIGHT)
    # 爆弾Surface（bd_img）から爆弾Rect（bd_rct）を抽出する
    bd_rct = bd_img.get_rect()
    # 爆弾Rectの中心座標を乱数で指定する
    bd_rct.center = x, y 
    vx, vy = +5, +5  # 練習２
    go_flag = 0  # ゲームオーバーになったか

    clock = pg.time.Clock()
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
            
        
        pg.draw.circle(bd_img, ((tmr % 255), 0, (255 - (tmr % 255))), (10, 10), 10)
        
        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]  # 合計移動量
        for k, mv in delta.items():
            if key_lst[k]: 
                sum_mv[0] += mv[0]
                sum_mv[1] += mv[1]
        
        kk_img_res = kk_img_lst[tuple(sum_mv)]  # 進行方向によって、こうかとんの向きを変える

        if kk_rct.colliderect(bd_rct) or go_flag == 1:  # 当たる
            if go_flag == 0:
                go_time = tmr  # ゲームオーバー時のタイムを記録
            kk_img_res = pg.image.load("ex02/fig/8.png")  # こうかとんのイラストを変える
            kk_img_res = pg.transform.rotozoom(kk_img_res, 0, 2.0)
            go_flag = 1  # ゲームオーバーした印

        if go_flag == 1 and go_time + 200 == tmr:  # ゲームオーバーから数秒後、強制終了する
            print("ゲームオーバー")
            return   # ゲームオーバー 
                
        kk_rct.move_ip(sum_mv)  # こうかとん移動
        if check_bound(kk_rct) != (True, True):  # こうかとんが画面外に行った
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])
 
        screen.blit(bg_img, [0, 0])
        screen.blit(kk_img_res, kk_rct)
        
        if tmr <= 2000 and tmr % 200 == 0:  # 定期的に爆弾の速度を早める(2000まで200ごとに作動; 合計10回)
            vx *= 1.5
            vy *= 1.5

        bd_rct.move_ip(vx, vy)  # 練習２
        yoko, tate = check_bound(bd_rct)
        if not yoko:  # 横方向に画面外だったら
            vx *= -1
        if not tate:  # 縦方向に範囲外だったら
            vy *= -1

        # 爆弾がこうかとんに近づくようにする
        if random.randint(0, 20) == 0:  # たまに近づく
            if ( ( kk_rct.left < bd_rct.left and vx > 0 )
                    or ( kk_rct.left > bd_rct.left and vx < 0)):
                vx *= -1
            if ( ( kk_rct.top < bd_rct.top and vy > 0 )
                    or ( kk_rct.top > bd_rct.top and vy < 0)):
                vy *= -1
            
        screen.blit(bd_img, bd_rct)
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()