/**
 * http://doc.rust-lang.org/stable/std/collections/struct.HashMap.html
 * https://github.com/rust-lang/rust/blob/1.0.0/src/test/run-pass/hashmap-memory.rs
 * https://github.com/rust-lang/rust/blob/1.0.0/src/libstd/collections/hash/map.rs
 *
 * @license MIT license <http://www.opensource.org/licenses/mit-license.php>
 */
use std::collections::HashMap;
use std::collections::hash_map::Entry::{Occupied, Vacant};

fn main() {
	println!("Using borrowed pointers as keys.");
	let mut h: HashMap<&str, isize>;
	h = HashMap::new();
}
