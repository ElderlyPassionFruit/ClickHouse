#pragma once

#include <AggregateFunctions/IAggregateFunction.h>
#include <AggregateFunctions/KeyHolderHelpers.h>
#include <Columns/ColumnArray.h>
#include "Common/HashTable/HashTableKeyHolder.h"
#include "Common/PODArray.h"
#include <Common/assert_cast.h>
#include <DataTypes/DataTypeArray.h>
#include <Interpreters/AggregationCommon.h>
#include <double-conversion/utils.h>
#include <Common/HashTable/HashMap.h>
#include <Common/SipHash.h>
#include "IO/WriteHelpers.h"


#define AGGREGATE_FUNCTION_GRAPH_MAX_SIZE 0xFFFFFF

namespace DB
{
struct Settings;

namespace ErrorCodes
{
    extern const int SET_SIZE_LIMIT_EXCEEDED;
}

struct GraphHeightGenericData
{
    HashMap<StringRef, StringRef> graph;

    void merge(GraphHeightGenericData & rhs) {
        for (const auto & elem : rhs.graph) {
            graph[elem.getKey()] = elem.getMapped();
            if (unlikely(graph.size() > AGGREGATE_FUNCTION_GRAPH_MAX_SIZE)) {
                throw Exception("Too large graph size", ErrorCodes::SET_SIZE_LIMIT_EXCEEDED);
            }
        }
    }

    void serialize(WriteBuffer & buf) const
    {
        writeVarUInt(graph.size(), buf);
        for (const auto & elem : graph) {
            writeStringBinary(elem.getKey(), buf);
            writeStringBinary(elem.getMapped(), buf);
        }
    }

    void deserialize(ReadBuffer & buf, Arena* arena)
    {
        size_t size;
        readVarUInt(size, buf);
        if (unlikely(size > AGGREGATE_FUNCTION_GRAPH_MAX_SIZE)) {
            throw Exception("Too large graph size to serialize", ErrorCodes::SET_SIZE_LIMIT_EXCEEDED);
        }
        for (size_t i = 0; i < size; ++i) {
            graph[readStringBinaryInto(*arena, buf)] = readStringBinaryInto(*arena, buf);
        }
    }

    void add(const IColumn ** columns, size_t row_num, Arena * arena)
    {
        const char * begin = nullptr;
        graph[columns[0]->serializeValueIntoArena(row_num, *arena, begin)] = columns[1]->serializeValueIntoArena(row_num, *arena, begin);
    }
};

/// Implementation of groupArray for String or any ComplexObject via Array
template <typename Node>
class GraphHeightGeneralImpl final
    : public IAggregateFunctionDataHelper<GraphHeightGenericData, GraphHeightGeneralImpl<Node>>
{
    using Data = GraphHeightGenericData;
    DataTypePtr & data_type;

public:
    GraphHeightGeneralImpl(const DataTypePtr & data_type_, const Array & parameters_)
        : IAggregateFunctionDataHelper<GraphHeightGenericData, GraphHeightGeneralImpl<Node>>(
            {data_type_}, parameters_)
        , data_type(this->argument_types[0])
    {
        assertNoParameters(getName(), this->parameters);
        assertBinary(getName(), this->argument_types);
    }

    String getName() const override { return "GraphHeight"; }

    DataTypePtr getReturnType() const override { return std::make_shared<DataTypeArray>(data_type); }

    void add(AggregateDataPtr __restrict place, const IColumn ** columns, size_t row_num, Arena * arena) const override
    {
        this->data(place).add(columns, row_num, arena);
    }

    void merge(AggregateDataPtr __restrict place, ConstAggregateDataPtr rhs, Arena *) const override
    {
        this->data(rhs).merge(this->data(rhs));
    }

    void serialize(ConstAggregateDataPtr __restrict place, WriteBuffer & buf, std::optional<size_t> /* version */) const override
    {
        this->data(place).serialize(buf);
    }

    void deserialize(AggregateDataPtr __restrict place, ReadBuffer & buf, std::optional<size_t> /* version */, Arena * arena) const override
    {
        this->data(place).deserialize(buf, arena);
    }

    void insertResultInto(AggregateDataPtr __restrict place, IColumn & to, Arena *) const override
    {
        // TODO
    }

    bool allocatesMemoryInArena() const override { return true; }
};


}
