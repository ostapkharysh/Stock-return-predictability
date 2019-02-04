package json;

/**
 * Created by Andrii_Rodionov on 1/3/2017.
 */
public class Tuple<K, V> {
    public final K key;
    public final V value;

    public Tuple(K key, V value) {
        this.key = key;
        this.value = value;
    }

    public K getKey() {
        return key;
    }

    public V getValue() {
        return value;
    }
}
