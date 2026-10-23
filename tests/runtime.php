<?php

declare(strict_types=1);

$required = [
    'bcmath', 'bz2', 'calendar', 'exif', 'gd', 'gmp', 'imagick', 'intl',
    'mongodb', 'mysqli', 'Zend OPcache', 'pcntl', 'pdo_mysql', 'pdo_pgsql',
    'pdo_sqlite', 'pgsql', 'redis', 'soap', 'sockets', 'xdebug', 'xsl', 'zip',
];
foreach ($required as $extension) {
    if (!extension_loaded($extension)) {
        throw new RuntimeException("Missing extension: {$extension}");
    }
}
if (extension_loaded('pcov')) {
    throw new RuntimeException('PCOV must not be loaded alongside Xdebug');
}
if (xdebug_info('mode') !== []) {
    throw new RuntimeException('Xdebug must be disabled by default');
}

// Laravel applications commonly use SQLite in CI.
$database = new PDO('sqlite::memory:');
if ($database->query('SELECT 1')->fetchColumn() != 1) {
    throw new RuntimeException('SQLite query failed');
}

// Exercise both the custom PDF policy and the Ghostscript delegate.
$pdf = tempnam(sys_get_temp_dir(), 'image-smoke-');
try {
    $image = new Imagick();
    $image->newImage(16, 16, 'white');
    $image->setImageFormat('pdf');
    $image->writeImage($pdf);
    $image->clear();
    $image->readImage($pdf);
    $image->setImageFormat('png');
    if (!str_starts_with($image->getImageBlob(), "\x89PNG\r\n\x1a\n")) {
        throw new RuntimeException('PDF to PNG conversion failed');
    }
} finally {
    unlink($pdf);
}
echo "Runtime smoke tests passed\n";
