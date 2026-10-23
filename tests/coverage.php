<?php

declare(strict_types=1);

if (!in_array('coverage', xdebug_info('mode'), true)) {
    throw new RuntimeException('Coverage mode is not active');
}
xdebug_start_code_coverage(XDEBUG_CC_UNUSED | XDEBUG_CC_DEAD_CODE);
require __DIR__ . '/coverage-fixture.php';
if (coverageFixture(2) !== 4) {
    throw new RuntimeException('Coverage fixture returned the wrong result');
}
$coverage = xdebug_get_code_coverage();
xdebug_stop_code_coverage();
$lines = $coverage[__DIR__ . '/coverage-fixture.php'] ?? [];
if (!in_array(1, $lines, true)) {
    throw new RuntimeException('No executed fixture lines were collected');
}
echo "Coverage smoke test passed\n";
