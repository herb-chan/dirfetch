pkgname=dirfetch
pkgver=1.0.5
pkgrel=1
pkgdesc="A customizable directory-fetching tool like neofetch"
arch=('any')
url="https://github.com/herb-chan/dirfetch"
license=('MIT')
depends=('python' 'python-rich')
makedepends=('python-setuptools' 'python-wheel' 'python-build')
source=("$pkgname-$pkgver.tar.gz::$url/archive/refs/tags/v$pkgver.tar.gz")
sha256sums=('SKIP')  # Placeholder for checksum, to be filled automatically by makepkg

build() {
  cd "$srcdir/$pkgname-$pkgver"
  python -m venv venv  # Create a virtual environment (optional, for building)
  source venv/bin/activate  # Activate the virtual environment
  pip install --upgrade pip setuptools wheel build  # Ensure build package is installed
  python -m build --wheel  # Build the package into a wheel
}

package() {
  cd "$srcdir/$pkgname-$pkgver"
  source venv/bin/activate  # Activate the virtual environment

  # Install the built wheel into the $pkgdir
  pip install --no-deps --root="$pkgdir" dist/*.whl
}
