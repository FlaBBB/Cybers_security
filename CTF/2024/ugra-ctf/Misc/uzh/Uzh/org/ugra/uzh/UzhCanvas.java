package org.ugra.uzh;

import java.io.ByteArrayOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import javax.microedition.io.Connector;
import javax.microedition.io.HttpConnection;
import javax.microedition.lcdui.Canvas;
import javax.microedition.lcdui.Font;
import javax.microedition.lcdui.Graphics;
import javax.microedition.lcdui.Image;

public class UzhCanvas extends Canvas implements Runnable {
    private long canvasId;
    private Thread thread;
    private UzhWorld world;
    private ByteArrayOutputStream outputStream;
    private byte direction = 1;
    private int score = -1;
    private int highScore = 0;
    private String message = "";
    private Font font;
    private Image image;
    private Graphics graphics;
    private int cellSize;
    private int offsetX;
    private int offsetY;
    private int gridWidth;
    private int gridHeight;

    public UzhCanvas(long canvasId) {
        this.canvasId = canvasId;
        int screenWidth = getWidth();
        int screenHeight = getHeight();
        this.font = Font.getDefaultFont();
        if (!isDoubleBuffered()) {
            this.image = Image.createImage(screenWidth, screenHeight);
            this.graphics = this.image.getGraphics();
            this.graphics.setFont(this.font);
        }

        int digitWidth = this.font.stringWidth("999");
        int horizontalCells = (screenWidth - 2 - 2 - digitWidth) / 40;
        int verticalCells = (screenHeight - 2) / 30;
        this.cellSize = Math.min(horizontalCells, verticalCells);
        horizontalCells = (screenWidth - this.cellSize * 40 - 2) / 2;
        screenWidth = screenWidth - this.cellSize * 40 - 2 - 2 - digitWidth;
        this.offsetX = Math.min(horizontalCells, screenWidth);
        this.offsetY = (screenHeight - this.cellSize * 30 - 2) / 2;
        this.gridWidth = 40 * this.cellSize;
        this.gridHeight = 30 * this.cellSize;
    }

    public void paint(Graphics g) {
        if (this.outputStream != null) {
            drawGame(this.graphics);
            g.drawImage(this.image, 0, 0, 20);
        } else {
            g.setFont(this.font);
            drawGame(g);
        }
    }

    private void drawGame(Graphics g) {
        g.setColor(255, 255, 255);
        g.fillRect(0, 0, getWidth(), getHeight());
        if (this.world != null) {
            drawGridLines(g);
            drawSnake(g);
            g.setColor(244, 193, 0);
            Point fruit = this.world.getFruit();
            drawCell(g, fruit.x, fruit.y, (byte) 1, (byte) 1);
            g.setColor(0, 0, 0);
            g.drawString(String.valueOf(this.world.getEatenFruits()), getWidth() - 1, this.offsetY, 24);
        } else {
            drawGameOver(g);
        }
    }

    private void drawGridLines(Graphics g) {
        g.setColor(0, 0, 0);
        g.fillRect(this.offsetX, this.offsetY, 2 + this.gridWidth, 1);
        g.fillRect(this.offsetX, this.offsetY, 1, 2 + this.gridHeight);
        g.fillRect(this.offsetX + 1 + this.gridWidth, this.offsetY, 1, 2 + this.gridHeight);
        g.fillRect(this.offsetX, this.offsetY + 1 + this.gridHeight, 2 + this.gridWidth, 1);
    }

    private void drawSnake(Graphics g) {
        g.setColor(0, 255, 0);
        UzhBody.Segment segment = this.world.getBody().getTailSegment();

        do {
            switch (segment.direction) {
                case -2:
                    drawCell(g, segment.head.x, (byte) (segment.head.y - segment.length + 1), (byte) 1, segment.length);
                    break;
                case -1:
                    drawCell(g, segment.head.x, segment.head.y, segment.length, (byte) 1);
                    break;
                case 1:
                    drawCell(g, (byte) (segment.head.x - segment.length + 1), segment.head.y, segment.length, (byte) 1);
                    break;
                case 2:
                    drawCell(g, segment.head.x, segment.head.y, (byte) 1, segment.length);
            }
        } while ((segment = segment.next) != null);
    }

    private void drawCell(Graphics g, byte x, byte y, byte width, byte height) {
        g.fillRect(this.offsetX + 1 + x * this.cellSize, this.offsetY + 1 + (30 - height - y) * this.cellSize,
                width * this.cellSize, height * this.cellSize);
    }

    private void drawGameOver(Graphics g) {
        int screenWidth = getWidth();
        int screenHeight = getHeight();
        int fontHeight = this.font.getHeight();
        g.setColor(0, 0, 0);
        screenWidth /= 2;
        screenHeight /= 3;
        g.drawString("High score:", screenWidth, screenHeight, 17);
        screenHeight += fontHeight;
        g.drawString(String.valueOf(this.highScore), screenWidth, screenHeight, 17);
        screenHeight += fontHeight + fontHeight / 2;
        if (this.score >= 0) {
            g.drawString("Last score:", screenWidth, screenHeight, 17);
            screenHeight += fontHeight;
            g.drawString(String.valueOf(this.score), screenWidth, screenHeight, 17);
        } else {
            screenHeight += fontHeight;
        }

        screenHeight += fontHeight + fontHeight / 2;
        String msg = (this.message != null) ? this.message : "Fetching results...";
        if (!msg.equals("")) {
            int start = 0;
            for (int end = msg.indexOf(10); end != -1; end = msg.indexOf(10, start)) {
                g.drawString(msg.substring(start, end), screenWidth, screenHeight, 17);
                screenHeight += fontHeight;
                start = end + 1;
            }
            g.drawString(msg.substring(start), screenWidth, screenHeight, 17);
        }
    }

    protected void keyPressed(int keyCode) {
        switch (keyCode) {
            case -4:
            case 5:
            case 54:
                this.direction = 1;
                break;
            case -3:
            case 2:
            case 52:
                this.direction = -1;
                break;
            case -2:
            case 6:
            case 56:
                this.direction = 2;
                break;
            case -1:
            case 1:
            case 50:
                this.direction = -2;
        }

        if (this.world == null && this.outputStream == null) {
            this.world = new UzhWorld(this.canvasId, this.direction);
            this.outputStream = new ByteArrayOutputStream();
            this.outputStream.write(this.direction);
            this.thread = new Thread(this);
            this.thread.start();
        }

    }

    public void run() {
        try {
            this.repaint();

            while (true) {
                try {
                    Thread.sleep((long) this.world.getStepDelay());
                } catch (InterruptedException e) {
                    System.err.println(e);
                }

                if (this.isShown()) {
                    byte nextDirection = this.direction;
                    byte headDirection = this.world.getBody().getHeadSegment().direction;
                    if (nextDirection == Point.invertDirection(headDirection)) {
                        nextDirection = headDirection;
                    }

                    this.outputStream.write(nextDirection);
                    if (!this.world.advance(nextDirection) || this.world.getEatenFruits() >= 10) {
                        this.score = this.world.getEatenFruits();
                        this.highScore = Math.max(this.highScore, this.score);
                        return;
                    }

                    this.repaint();
                }
            }
        } finally {
            this.cleanup();
        }
    }

    private void cleanup() {
        this.outputStream = null;
        this.message = "Fetching...";
        this.repaint();

        try {
            HttpConnection connection = (HttpConnection) Connector.open("http://q.2024.ugractf.ru:9276/scores/?secret=" + this.canvasId);

            try {
                connection.setRequestMethod("POST");
                connection.setRequestProperty("Content-Type", "application/octet-stream");
                OutputStream os = connection.openOutputStream();
                os.write(this.outputStream.toByteArray());
                os.close();
                int responseCode = connection.getResponseCode();
                if (responseCode != 200) {
                    this.message = "Error " + responseCode + ": " + connection.getResponseMessage();
                } else {
                    InputStream is = connection.openInputStream();
                    ByteArrayOutputStream bos = new ByteArrayOutputStream();
                    byte[] buffer = new byte[128];
                    int bytesRead;
                    while ((bytesRead = is.read(buffer)) != -1) {
                        bos.write(buffer, 0, bytesRead);
                    }
                    is.close();
                    this.message = bos.toString();
                }
            } finally {
                connection.close();
            }
        } catch (IOException e) {
            this.message = e.toString();
        }

        this.repaint();
        this.outputStream = null;
    }
}
