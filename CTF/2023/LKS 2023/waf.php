<?php
class WAF
{
    const attempts = 200;
    const outTime = 2;
    const path = "/var/www/data/";
    const dbFile = "waf.db.txt";
    const blFile = "waf.bl.txt";

    private static function loadClean($dbf)
    {
        $dbf = self::path . $dbf;

        if (file_exists($dbf)) {
            $db = unserialize(file_get_contents($dbf));
        } else {
            if (!is_dir(self::path)) {
                mkdir(self::path);
            }
        }

        if (!is_array($db)) {
            $db = array();
        }

        foreach ($db as $row => $sub_array) {
            if ($sub_array['time'] < time()) {
                unset($db[$row]);
            }
        }

        file_put_contents($dbf, serialize($db));
        return $db;
    }

    private static function check($db)
    {
        if (is_array($db)) {
            if (count($db) > 1) {
                return array_count_values(array_column($db, 'ip'))[$_SERVER['REMOTE_ADDR']];
            }
        } else {
            return 0;
        }
    }

    private static function write($db, $dbf)
    {
        file_put_contents(self::path . $dbf, serialize($db));
    }

    private static function add($db, $tm = 1)
    {
        array_push($db, ['time' => time() + (60 * $tm), 'ip' => $_SERVER['REMOTE_ADDR']]);
        return $db;
    }

    public static function DoWAF($hit)
    {
        while (!@mkdir(self::path . 'db.lock', 0777)) {
            usleep(100000);
        }

        $db = self::loadClean(self::dbFile);
        $bl = self::loadClean(self::blFile);

        if (self::check($bl) > 0) {
            self::forbidden();
        } else if ($hit > 0) {
            $db = self::add($db);
            self::write($db, self::dbFile);

            if (self::check($db) >= self::attempts) {
                self::write(self::add($bl, self::outTime), self::blFile);
            }

            if ($hit == 403) {
                self::forbidden();
            } else {
                self::notfound();
            }
        }
        rmdir(self::path . 'db.lock');
    }

    public static function forbidden()
    {
        rmdir(self::path . 'db.lock');
        header('HTTP/1.0 403 Forbidden', true, 403);
        die('<h1>Forbidden</h1>');
    }

    public static function notfound()
    {
        rmdir(self::path . 'db.lock');
        header('HTTP/1.0 404 Not Found', true, 404);
        die('<h1>Not Found</h1>');
    }
}

WAF::DoWAF(isset($_GET['e']) ? $_GET['e'] : 0);
