#include "AggregateFunctionGraphOperation.h"

namespace DB
{

namespace ErrorCodes {
  extern const int UNSUPPORTED_PARAMETER;
}

class GraphComponentsCountGeneral final : public GraphOperationGeneral<BidirectionalGraphGenericData, GraphComponentsCountGeneral>
{
public:
    using GraphOperationGeneral<BidirectionalGraphGenericData, GraphComponentsCountGeneral>::GraphOperationGeneral;

    static constexpr const char* name = "graphComponentsCount";

    DataTypePtr getReturnType() const override { return std::make_shared<DataTypeUInt64>(); }

    UInt64 calculateOperation(ConstAggregateDataPtr __restrict place, Arena*) const {
        return this->data(place).componentsCount();
    }
};

template void registerGraphAggregateFunction<GraphComponentsCountGeneral>(AggregateFunctionFactory & factory);

}
