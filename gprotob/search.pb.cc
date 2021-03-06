// Generated by the protocol buffer compiler.  DO NOT EDIT!
// source: search.proto

#include "search.pb.h"

#include <algorithm>

#include <google/protobuf/stubs/common.h>
#include <google/protobuf/stubs/port.h>
#include <google/protobuf/io/coded_stream.h>
#include <google/protobuf/wire_format_lite_inl.h>
#include <google/protobuf/descriptor.h>
#include <google/protobuf/generated_message_reflection.h>
#include <google/protobuf/reflection_ops.h>
#include <google/protobuf/wire_format.h>
// This is a temporary google only hack
#ifdef GOOGLE_PROTOBUF_ENFORCE_UNIQUENESS
#include "third_party/protobuf/version.h"
#endif
// @@protoc_insertion_point(includes)

namespace eg {
class SearchRequestDefaultTypeInternal {
 public:
  ::google::protobuf::internal::ExplicitlyConstructed<SearchRequest>
      _instance;
} _SearchRequest_default_instance_;
}  // namespace eg
namespace protobuf_search_2eproto {
static void InitDefaultsSearchRequest() {
  GOOGLE_PROTOBUF_VERIFY_VERSION;

  {
    void* ptr = &::eg::_SearchRequest_default_instance_;
    new (ptr) ::eg::SearchRequest();
    ::google::protobuf::internal::OnShutdownDestroyMessage(ptr);
  }
  ::eg::SearchRequest::InitAsDefaultInstance();
}

::google::protobuf::internal::SCCInfo<0> scc_info_SearchRequest =
    {{ATOMIC_VAR_INIT(::google::protobuf::internal::SCCInfoBase::kUninitialized), 0, InitDefaultsSearchRequest}, {}};

void InitDefaults() {
  ::google::protobuf::internal::InitSCC(&scc_info_SearchRequest.base);
}

::google::protobuf::Metadata file_level_metadata[1];

const ::google::protobuf::uint32 TableStruct::offsets[] GOOGLE_PROTOBUF_ATTRIBUTE_SECTION_VARIABLE(protodesc_cold) = {
  GOOGLE_PROTOBUF_GENERATED_MESSAGE_FIELD_OFFSET(::eg::SearchRequest, _has_bits_),
  GOOGLE_PROTOBUF_GENERATED_MESSAGE_FIELD_OFFSET(::eg::SearchRequest, _internal_metadata_),
  ~0u,  // no _extensions_
  ~0u,  // no _oneof_case_
  ~0u,  // no _weak_field_map_
  GOOGLE_PROTOBUF_GENERATED_MESSAGE_FIELD_OFFSET(::eg::SearchRequest, query_),
  GOOGLE_PROTOBUF_GENERATED_MESSAGE_FIELD_OFFSET(::eg::SearchRequest, page_number_),
  GOOGLE_PROTOBUF_GENERATED_MESSAGE_FIELD_OFFSET(::eg::SearchRequest, result_per_page_),
  0,
  1,
  2,
};
static const ::google::protobuf::internal::MigrationSchema schemas[] GOOGLE_PROTOBUF_ATTRIBUTE_SECTION_VARIABLE(protodesc_cold) = {
  { 0, 8, sizeof(::eg::SearchRequest)},
};

static ::google::protobuf::Message const * const file_default_instances[] = {
  reinterpret_cast<const ::google::protobuf::Message*>(&::eg::_SearchRequest_default_instance_),
};

void protobuf_AssignDescriptors() {
  AddDescriptors();
  AssignDescriptors(
      "search.proto", schemas, file_default_instances, TableStruct::offsets,
      file_level_metadata, NULL, NULL);
}

void protobuf_AssignDescriptorsOnce() {
  static ::google::protobuf::internal::once_flag once;
  ::google::protobuf::internal::call_once(once, protobuf_AssignDescriptors);
}

void protobuf_RegisterTypes(const ::std::string&) GOOGLE_PROTOBUF_ATTRIBUTE_COLD;
void protobuf_RegisterTypes(const ::std::string&) {
  protobuf_AssignDescriptorsOnce();
  ::google::protobuf::internal::RegisterAllTypes(file_level_metadata, 1);
}

void AddDescriptorsImpl() {
  InitDefaults();
  static const char descriptor[] GOOGLE_PROTOBUF_ATTRIBUTE_SECTION_VARIABLE(protodesc_cold) = {
      "\n\014search.proto\022\002eg\"L\n\rSearchRequest\022\r\n\005q"
      "uery\030\001 \002(\t\022\023\n\013page_number\030\002 \001(\005\022\027\n\017resul"
      "t_per_page\030\003 \001(\005"
  };
  ::google::protobuf::DescriptorPool::InternalAddGeneratedFile(
      descriptor, 96);
  ::google::protobuf::MessageFactory::InternalRegisterGeneratedFile(
    "search.proto", &protobuf_RegisterTypes);
}

void AddDescriptors() {
  static ::google::protobuf::internal::once_flag once;
  ::google::protobuf::internal::call_once(once, AddDescriptorsImpl);
}
// Force AddDescriptors() to be called at dynamic initialization time.
struct StaticDescriptorInitializer {
  StaticDescriptorInitializer() {
    AddDescriptors();
  }
} static_descriptor_initializer;
}  // namespace protobuf_search_2eproto
namespace eg {

// ===================================================================

void SearchRequest::InitAsDefaultInstance() {
}
#if !defined(_MSC_VER) || _MSC_VER >= 1900
const int SearchRequest::kQueryFieldNumber;
const int SearchRequest::kPageNumberFieldNumber;
const int SearchRequest::kResultPerPageFieldNumber;
#endif  // !defined(_MSC_VER) || _MSC_VER >= 1900

SearchRequest::SearchRequest()
  : ::google::protobuf::Message(), _internal_metadata_(NULL) {
  ::google::protobuf::internal::InitSCC(
      &protobuf_search_2eproto::scc_info_SearchRequest.base);
  SharedCtor();
  // @@protoc_insertion_point(constructor:eg.SearchRequest)
}
SearchRequest::SearchRequest(const SearchRequest& from)
  : ::google::protobuf::Message(),
      _internal_metadata_(NULL),
      _has_bits_(from._has_bits_) {
  _internal_metadata_.MergeFrom(from._internal_metadata_);
  query_.UnsafeSetDefault(&::google::protobuf::internal::GetEmptyStringAlreadyInited());
  if (from.has_query()) {
    query_.AssignWithDefault(&::google::protobuf::internal::GetEmptyStringAlreadyInited(), from.query_);
  }
  ::memcpy(&page_number_, &from.page_number_,
    static_cast<size_t>(reinterpret_cast<char*>(&result_per_page_) -
    reinterpret_cast<char*>(&page_number_)) + sizeof(result_per_page_));
  // @@protoc_insertion_point(copy_constructor:eg.SearchRequest)
}

void SearchRequest::SharedCtor() {
  query_.UnsafeSetDefault(&::google::protobuf::internal::GetEmptyStringAlreadyInited());
  ::memset(&page_number_, 0, static_cast<size_t>(
      reinterpret_cast<char*>(&result_per_page_) -
      reinterpret_cast<char*>(&page_number_)) + sizeof(result_per_page_));
}

SearchRequest::~SearchRequest() {
  // @@protoc_insertion_point(destructor:eg.SearchRequest)
  SharedDtor();
}

void SearchRequest::SharedDtor() {
  query_.DestroyNoArena(&::google::protobuf::internal::GetEmptyStringAlreadyInited());
}

void SearchRequest::SetCachedSize(int size) const {
  _cached_size_.Set(size);
}
const ::google::protobuf::Descriptor* SearchRequest::descriptor() {
  ::protobuf_search_2eproto::protobuf_AssignDescriptorsOnce();
  return ::protobuf_search_2eproto::file_level_metadata[kIndexInFileMessages].descriptor;
}

const SearchRequest& SearchRequest::default_instance() {
  ::google::protobuf::internal::InitSCC(&protobuf_search_2eproto::scc_info_SearchRequest.base);
  return *internal_default_instance();
}


void SearchRequest::Clear() {
// @@protoc_insertion_point(message_clear_start:eg.SearchRequest)
  ::google::protobuf::uint32 cached_has_bits = 0;
  // Prevent compiler warnings about cached_has_bits being unused
  (void) cached_has_bits;

  cached_has_bits = _has_bits_[0];
  if (cached_has_bits & 0x00000001u) {
    query_.ClearNonDefaultToEmptyNoArena();
  }
  if (cached_has_bits & 6u) {
    ::memset(&page_number_, 0, static_cast<size_t>(
        reinterpret_cast<char*>(&result_per_page_) -
        reinterpret_cast<char*>(&page_number_)) + sizeof(result_per_page_));
  }
  _has_bits_.Clear();
  _internal_metadata_.Clear();
}

bool SearchRequest::MergePartialFromCodedStream(
    ::google::protobuf::io::CodedInputStream* input) {
#define DO_(EXPRESSION) if (!GOOGLE_PREDICT_TRUE(EXPRESSION)) goto failure
  ::google::protobuf::uint32 tag;
  // @@protoc_insertion_point(parse_start:eg.SearchRequest)
  for (;;) {
    ::std::pair<::google::protobuf::uint32, bool> p = input->ReadTagWithCutoffNoLastTag(127u);
    tag = p.first;
    if (!p.second) goto handle_unusual;
    switch (::google::protobuf::internal::WireFormatLite::GetTagFieldNumber(tag)) {
      // required string query = 1;
      case 1: {
        if (static_cast< ::google::protobuf::uint8>(tag) ==
            static_cast< ::google::protobuf::uint8>(10u /* 10 & 0xFF */)) {
          DO_(::google::protobuf::internal::WireFormatLite::ReadString(
                input, this->mutable_query()));
          ::google::protobuf::internal::WireFormat::VerifyUTF8StringNamedField(
            this->query().data(), static_cast<int>(this->query().length()),
            ::google::protobuf::internal::WireFormat::PARSE,
            "eg.SearchRequest.query");
        } else {
          goto handle_unusual;
        }
        break;
      }

      // optional int32 page_number = 2;
      case 2: {
        if (static_cast< ::google::protobuf::uint8>(tag) ==
            static_cast< ::google::protobuf::uint8>(16u /* 16 & 0xFF */)) {
          set_has_page_number();
          DO_((::google::protobuf::internal::WireFormatLite::ReadPrimitive<
                   ::google::protobuf::int32, ::google::protobuf::internal::WireFormatLite::TYPE_INT32>(
                 input, &page_number_)));
        } else {
          goto handle_unusual;
        }
        break;
      }

      // optional int32 result_per_page = 3;
      case 3: {
        if (static_cast< ::google::protobuf::uint8>(tag) ==
            static_cast< ::google::protobuf::uint8>(24u /* 24 & 0xFF */)) {
          set_has_result_per_page();
          DO_((::google::protobuf::internal::WireFormatLite::ReadPrimitive<
                   ::google::protobuf::int32, ::google::protobuf::internal::WireFormatLite::TYPE_INT32>(
                 input, &result_per_page_)));
        } else {
          goto handle_unusual;
        }
        break;
      }

      default: {
      handle_unusual:
        if (tag == 0) {
          goto success;
        }
        DO_(::google::protobuf::internal::WireFormat::SkipField(
              input, tag, _internal_metadata_.mutable_unknown_fields()));
        break;
      }
    }
  }
success:
  // @@protoc_insertion_point(parse_success:eg.SearchRequest)
  return true;
failure:
  // @@protoc_insertion_point(parse_failure:eg.SearchRequest)
  return false;
#undef DO_
}

void SearchRequest::SerializeWithCachedSizes(
    ::google::protobuf::io::CodedOutputStream* output) const {
  // @@protoc_insertion_point(serialize_start:eg.SearchRequest)
  ::google::protobuf::uint32 cached_has_bits = 0;
  (void) cached_has_bits;

  cached_has_bits = _has_bits_[0];
  // required string query = 1;
  if (cached_has_bits & 0x00000001u) {
    ::google::protobuf::internal::WireFormat::VerifyUTF8StringNamedField(
      this->query().data(), static_cast<int>(this->query().length()),
      ::google::protobuf::internal::WireFormat::SERIALIZE,
      "eg.SearchRequest.query");
    ::google::protobuf::internal::WireFormatLite::WriteStringMaybeAliased(
      1, this->query(), output);
  }

  // optional int32 page_number = 2;
  if (cached_has_bits & 0x00000002u) {
    ::google::protobuf::internal::WireFormatLite::WriteInt32(2, this->page_number(), output);
  }

  // optional int32 result_per_page = 3;
  if (cached_has_bits & 0x00000004u) {
    ::google::protobuf::internal::WireFormatLite::WriteInt32(3, this->result_per_page(), output);
  }

  if (_internal_metadata_.have_unknown_fields()) {
    ::google::protobuf::internal::WireFormat::SerializeUnknownFields(
        _internal_metadata_.unknown_fields(), output);
  }
  // @@protoc_insertion_point(serialize_end:eg.SearchRequest)
}

::google::protobuf::uint8* SearchRequest::InternalSerializeWithCachedSizesToArray(
    bool deterministic, ::google::protobuf::uint8* target) const {
  (void)deterministic; // Unused
  // @@protoc_insertion_point(serialize_to_array_start:eg.SearchRequest)
  ::google::protobuf::uint32 cached_has_bits = 0;
  (void) cached_has_bits;

  cached_has_bits = _has_bits_[0];
  // required string query = 1;
  if (cached_has_bits & 0x00000001u) {
    ::google::protobuf::internal::WireFormat::VerifyUTF8StringNamedField(
      this->query().data(), static_cast<int>(this->query().length()),
      ::google::protobuf::internal::WireFormat::SERIALIZE,
      "eg.SearchRequest.query");
    target =
      ::google::protobuf::internal::WireFormatLite::WriteStringToArray(
        1, this->query(), target);
  }

  // optional int32 page_number = 2;
  if (cached_has_bits & 0x00000002u) {
    target = ::google::protobuf::internal::WireFormatLite::WriteInt32ToArray(2, this->page_number(), target);
  }

  // optional int32 result_per_page = 3;
  if (cached_has_bits & 0x00000004u) {
    target = ::google::protobuf::internal::WireFormatLite::WriteInt32ToArray(3, this->result_per_page(), target);
  }

  if (_internal_metadata_.have_unknown_fields()) {
    target = ::google::protobuf::internal::WireFormat::SerializeUnknownFieldsToArray(
        _internal_metadata_.unknown_fields(), target);
  }
  // @@protoc_insertion_point(serialize_to_array_end:eg.SearchRequest)
  return target;
}

size_t SearchRequest::ByteSizeLong() const {
// @@protoc_insertion_point(message_byte_size_start:eg.SearchRequest)
  size_t total_size = 0;

  if (_internal_metadata_.have_unknown_fields()) {
    total_size +=
      ::google::protobuf::internal::WireFormat::ComputeUnknownFieldsSize(
        _internal_metadata_.unknown_fields());
  }
  // required string query = 1;
  if (has_query()) {
    total_size += 1 +
      ::google::protobuf::internal::WireFormatLite::StringSize(
        this->query());
  }
  if (_has_bits_[0 / 32] & 6u) {
    // optional int32 page_number = 2;
    if (has_page_number()) {
      total_size += 1 +
        ::google::protobuf::internal::WireFormatLite::Int32Size(
          this->page_number());
    }

    // optional int32 result_per_page = 3;
    if (has_result_per_page()) {
      total_size += 1 +
        ::google::protobuf::internal::WireFormatLite::Int32Size(
          this->result_per_page());
    }

  }
  int cached_size = ::google::protobuf::internal::ToCachedSize(total_size);
  SetCachedSize(cached_size);
  return total_size;
}

void SearchRequest::MergeFrom(const ::google::protobuf::Message& from) {
// @@protoc_insertion_point(generalized_merge_from_start:eg.SearchRequest)
  GOOGLE_DCHECK_NE(&from, this);
  const SearchRequest* source =
      ::google::protobuf::internal::DynamicCastToGenerated<const SearchRequest>(
          &from);
  if (source == NULL) {
  // @@protoc_insertion_point(generalized_merge_from_cast_fail:eg.SearchRequest)
    ::google::protobuf::internal::ReflectionOps::Merge(from, this);
  } else {
  // @@protoc_insertion_point(generalized_merge_from_cast_success:eg.SearchRequest)
    MergeFrom(*source);
  }
}

void SearchRequest::MergeFrom(const SearchRequest& from) {
// @@protoc_insertion_point(class_specific_merge_from_start:eg.SearchRequest)
  GOOGLE_DCHECK_NE(&from, this);
  _internal_metadata_.MergeFrom(from._internal_metadata_);
  ::google::protobuf::uint32 cached_has_bits = 0;
  (void) cached_has_bits;

  cached_has_bits = from._has_bits_[0];
  if (cached_has_bits & 7u) {
    if (cached_has_bits & 0x00000001u) {
      set_has_query();
      query_.AssignWithDefault(&::google::protobuf::internal::GetEmptyStringAlreadyInited(), from.query_);
    }
    if (cached_has_bits & 0x00000002u) {
      page_number_ = from.page_number_;
    }
    if (cached_has_bits & 0x00000004u) {
      result_per_page_ = from.result_per_page_;
    }
    _has_bits_[0] |= cached_has_bits;
  }
}

void SearchRequest::CopyFrom(const ::google::protobuf::Message& from) {
// @@protoc_insertion_point(generalized_copy_from_start:eg.SearchRequest)
  if (&from == this) return;
  Clear();
  MergeFrom(from);
}

void SearchRequest::CopyFrom(const SearchRequest& from) {
// @@protoc_insertion_point(class_specific_copy_from_start:eg.SearchRequest)
  if (&from == this) return;
  Clear();
  MergeFrom(from);
}

bool SearchRequest::IsInitialized() const {
  if ((_has_bits_[0] & 0x00000001) != 0x00000001) return false;
  return true;
}

void SearchRequest::Swap(SearchRequest* other) {
  if (other == this) return;
  InternalSwap(other);
}
void SearchRequest::InternalSwap(SearchRequest* other) {
  using std::swap;
  query_.Swap(&other->query_, &::google::protobuf::internal::GetEmptyStringAlreadyInited(),
    GetArenaNoVirtual());
  swap(page_number_, other->page_number_);
  swap(result_per_page_, other->result_per_page_);
  swap(_has_bits_[0], other->_has_bits_[0]);
  _internal_metadata_.Swap(&other->_internal_metadata_);
}

::google::protobuf::Metadata SearchRequest::GetMetadata() const {
  protobuf_search_2eproto::protobuf_AssignDescriptorsOnce();
  return ::protobuf_search_2eproto::file_level_metadata[kIndexInFileMessages];
}


// @@protoc_insertion_point(namespace_scope)
}  // namespace eg
namespace google {
namespace protobuf {
template<> GOOGLE_PROTOBUF_ATTRIBUTE_NOINLINE ::eg::SearchRequest* Arena::CreateMaybeMessage< ::eg::SearchRequest >(Arena* arena) {
  return Arena::CreateInternal< ::eg::SearchRequest >(arena);
}
}  // namespace protobuf
}  // namespace google

// @@protoc_insertion_point(global_scope)
