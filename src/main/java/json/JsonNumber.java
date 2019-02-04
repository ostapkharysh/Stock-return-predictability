package json;

/**
 * Created by Andrii_Rodionov on 1/3/2017.
 */
public class JsonNumber extends Json {
    private final Number number;

    public JsonNumber(Number number) {
        this.number = number;
    }

    @Override
    public String toJson() {
        return number.toString();
    }
}
