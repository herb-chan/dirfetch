pkgname=dirfetch
pkgver=1.0.0
pkgrel=1
pkgdesc="A customizable directory-fetching tool like neofetch"
arch=('any')
url="https://github.com/herb-chan/dirfetch"
license=('MIT')
depends=('python' 'python-rich')
source=("$pkgname-$pkgver.tar.gz::$url/archive/refs/tags/v$pkgver.tar.gz")
sha256sums=('SKIP')  # Replace with the actual checksum

build() {
  cd "$srcdir/$pkgname-$pkgver"
  python -m build --no-isolation --wheel
}

package() {
  cd "$srcdir/$pkgname-$pkgver"
  python -m installer --destdir="$pkgdir" dist/*.whl
}
