package ua.edu.ucu;

import org.junit.Before;
import org.junit.Test;
import ua.edu.ucu.stream.AsIntStream;
import ua.edu.ucu.stream.IntStream;

import static org.junit.Assert.assertArrayEquals;
import static org.junit.Assert.assertEquals;

/**
 * @author andrii
 */
public class StreamAppTest {

    private IntStream intStream;

    @Before
    public void init() {
        int[] intArr = {-1, 0, 1, 2, 3};
        intStream = AsIntStream.of(intArr);
    }

    @Test
    public void testStreamOperations() {
        System.out.println("streamOperations");
        int expResult = 42;
        int result = StreamApp.streamOperations(intStream);
        assertEquals(expResult, result);
    }

    @Test
    public void testStreamOperations2() {
        System.out.println("streamOperations");
        IntStream expResult = AsIntStream.of(1, 2, 3);
        IntStream output = AsIntStream.of(-1, 0, 1, 2, 3);
        IntStream result = output.filter(x -> x > 0);
        assertArrayEquals(expResult.toArray(), result.toArray());
    }

    @Test
    public void testStreamOperations3() {
        System.out.println("streamOperations");
        IntStream expResult = AsIntStream.of(1, 4, 9);
        IntStream output = AsIntStream.of(1, 2, 3);
        IntStream result = output.map(x -> x * x);
        assertArrayEquals(expResult.toArray(), result.toArray());
    }

    @Test
    public void testStreamOperations4() {
        System.out.println("streamOperations");
        IntStream expResult = AsIntStream.of(0, 1, 2, 3, 4, 5, 8, 9, 10);
        IntStream output = AsIntStream.of(1, 4, 9);
        IntStream result = output.flatMap(x -> AsIntStream.of(x - 1, x, x + 1));
        assertArrayEquals(expResult.toArray(), result.toArray());
    }

    @Test
    public void testStreamToArray() {
        System.out.println("streamToArray");
        int[] expResult = {-1, 0, 1, 2, 3};
        int[] result = StreamApp.streamToArray(intStream);
        assertArrayEquals(expResult, result);
    }

    @Test
    public void testStreamForEach() {
        System.out.println("streamForEach");
        String expResult = "-10123";
        String result = StreamApp.streamForEach(intStream);
        assertEquals(expResult, result);
    }

    @Test
    public void testEverage() {
        System.out.println("streamForEach");
        double expResult = 1.0;
        double result = intStream.average();
        assertEquals(expResult, (Object) result);
    }

    @Test
    public void testMin() {
        System.out.println("streamForEach");
        double expResult = -1;
        double result = intStream.min();
        assertEquals(expResult, (Object) result);
    }

    @Test
    public void testMax() {
        System.out.println("streamForEach");
        double expResult = 3;
        double result = intStream.max();
        assertEquals(expResult, (Object) result);
    }

    @Test
    public void testSum() {
        System.out.println("streamForEach");
        double expResult = 5;
        double result = intStream.sum();
        assertEquals(expResult, (Object) result);
    }

    @Test(expected = IllegalArgumentException.class)
    public void testMaxO() {
        IntStream intStrm = AsIntStream.of();
        System.out.println("streamForEach");
        intStrm.max();
    }

    @Test(expected = IllegalArgumentException.class)
    public void testMinO() {
        IntStream intStrm = AsIntStream.of();
        System.out.println("streamForEach");
        intStrm.min();
    }

    @Test(expected = IllegalArgumentException.class)
    public void testEverageO() {
        IntStream intStrm = AsIntStream.of();
        System.out.println("streamForEach");
        intStrm.average();
    }

    @Test(expected = IllegalArgumentException.class)
    public void testSumO() {
        IntStream intStrm = AsIntStream.of();
        System.out.println("streamForEach");
        intStrm.sum();
    }
}
