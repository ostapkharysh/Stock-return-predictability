package ua.edu.ucu.stream;

import ua.edu.ucu.function.*;

import java.util.ArrayList;

public class AsIntStream implements IntStream {

    private ArrayList<Integer> lstOfIntegers;

    private AsIntStream() {
        this.lstOfIntegers = new ArrayList<Integer>();
    }

    public static IntStream of(int... values) {
        AsIntStream stream = new AsIntStream();
        for (int val : values) {
            stream.lstOfIntegers.add(val);
        }
        return stream;
    }


    @Override
    public Double average() {
        if (lstOfIntegers.isEmpty()) {
            throw new IllegalArgumentException("Is Empty!");
        }
        return (double) sum() / count();
    }

    @Override
    public Integer max() {
        if (lstOfIntegers.isEmpty()) {
            throw new IllegalArgumentException("Is Empty!");
        }
        int output = lstOfIntegers.get(0);
        IntBinaryOperator op = (left, right) -> {
            if (right > left) {
                left = right;
            }
            return left;

        };
        return reduce(output, op);
    }

    @Override
    public Integer min() {
        if (lstOfIntegers.isEmpty()) {
            throw new IllegalArgumentException("Is Empty!");
        }
        int output = lstOfIntegers.get(0);
        IntBinaryOperator op = (left, right) -> {
            if (right < left) {
                left = right;
            }
            return left;

        };
        return reduce(output, op);
    }

    @Override
    public long count() {
        return lstOfIntegers.size();
    }

    @Override
    public Integer sum() {
        if (lstOfIntegers.isEmpty()) {
            throw new IllegalArgumentException("Is Empty!");
        }
        int output = 0;
        IntBinaryOperator op = (left, right) -> {
            left += right;
            return left;
        };
        return reduce(output, op);
    }

    @Override
    public IntStream filter(IntPredicate predicate) {
        AsIntStream out = new AsIntStream();
        for (int intgrs : lstOfIntegers) {
            if (predicate.test(intgrs)) {
                out.lstOfIntegers.add(intgrs);
            }
        }
        return out;
    }

    @Override
    public void forEach(IntConsumer action) {

        for (int intgr : lstOfIntegers) {
            action.accept(intgr);
        }
    }

    @Override
    public IntStream map(IntUnaryOperator mapper) {
        AsIntStream stream = new AsIntStream();
        forEach(x -> {
            stream.lstOfIntegers.add(mapper.apply(x));
        });
        return stream;
    }

    @Override
    public IntStream flatMap(IntToIntStreamFunction func) {
        ArrayList<Integer> temp = new ArrayList<>();
        this.forEach(
                x -> {
                    AsIntStream ar = (AsIntStream) func.applyAsIntStream(x);
                    IntConsumer action = temp::add;
                    ar.forEach(action);
                });
        int[] output = new int[temp.size()];
        for (int i = 0; i < temp.size(); i++) {
            output[i] = temp.get(i);
        }
        return AsIntStream.of(output);
    }

    @Override
    public int reduce(int identity, IntBinaryOperator op) {
        int result = identity;
        for (int element : lstOfIntegers) {
            result = op.apply(result, element);
        }
        return result;
    }

    @Override
    public int[] toArray() {
        int[] output = new int[(int) count()];
        for (int i = 0; i < count(); i++) {
            output[i] = lstOfIntegers.get(i);
        }
        return output;
    }

}
